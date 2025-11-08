import re
from typing import Optional, Dict, Any, List, Union
from urllib.parse import urlparse

# Mapping constants
RACE_TO_GENETICS = {
    'sativa': {'sativa': 100, 'indica': 0},
    'indica': {'sativa': 0, 'indica': 100},
    'hybrid': {'sativa': 50, 'indica': 50},
    'ruderalis': {'sativa': 0, 'indica': 0}, # Ruderalis is typically autoflower, genetics are 0/0
}

def normalize_country_code(country: Optional[str]) -> Optional[str]:
    """
    Normalizes country string (e.g., 'us', 'USA', 'united states') to Title Case.
    """
    if not country or not isinstance(country, str):
        return None
    
    country = country.strip()
    if not country:
        return None
    
    # Simple normalization to Title Case for consistency
    return country.title()

def validate_and_normalize_url(url: Optional[str]) -> Optional[str]:
    """
    Validates and normalizes a URL, ensuring it has a scheme.
    """
    if not url or not isinstance(url, str):
        return None
    
    url = url.strip()
    if not url:
        return None
    
    # Check if URL has a scheme (http or https)
    parsed = urlparse(url)
    if not parsed.scheme:
        # Assume https if no scheme is present
        url = f"https://{url}"
    
    # Basic validation (Pydantic models will handle deeper validation)
    if not re.match(r'^https?://', url):
        return None
        
    return url


def parse_percentage_value(value: Optional[Union[str, int, float]]) -> Optional[float]:
    """
    Parse cannabinoid percentage values (THC/CBD).

    Rules:
    - If value is None or empty string -> return None.
    - If numeric (int/float) -> return float(value).
    - If string:
      - Strip whitespace and trailing '%' if present.
      - If the string is a single numeric token -> return float(token).
      - If the string represents a numeric range (contains '-' or '–') -> return None.
      - If parsing fails -> return None.
    """
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    if not isinstance(value, str):
        return None

    s = value.strip()
    if not s:
        return None

    # Remove trailing percent sign and trim again
    if s.endswith('%'):
        s = s[:-1].strip()

    # If the input contains a hyphen or en-dash, treat as a range -> return None
    if '-' in s or '–' in s:
        # Quick validation: if it looks like a numeric range (e.g., "18-22"),
        # return None without computing a mean.
        parts = re.split(r'[-–]', s)
        if len(parts) == 2:
            try:
                # ensure both sides are numeric; we still return None for ranges
                float(parts[0].strip())
                float(parts[1].strip())
                return None
            except ValueError:
                # If not a clean numeric range, fall through to single-value parse attempt
                pass
        else:
            return None

    # Attempt to parse as a single numeric value
    try:
        return float(s)
    except ValueError:
        return None





def parse_race_to_genetics(race: Optional[str]) -> Dict[str, int]:
    """
    Maps API 'race' field (e.g., 'sativa', 'hybrid') to indica/sativa percentages.
    Returns default hybrid if race is unknown or None.
    """
    if not race or not isinstance(race, str):
        return RACE_TO_GENETICS['hybrid']
    
    race_lower = race.lower().strip()
    
    if race_lower in RACE_TO_GENETICS:
        return RACE_TO_GENETICS[race_lower]
    
    # Handle hybrid percentages if provided (e.g., 'sativa 60% / indica 40%')
    match = re.search(r'sativa\s*(\d+)%\s*/\s*indica\s*(\d+)%', race_lower)
    if match:
        sativa_pct = int(match.group(1))
        indica_pct = int(match.group(2))
        if sativa_pct + indica_pct <= 100:
            return {'sativa': sativa_pct, 'indica': indica_pct}

    return RACE_TO_GENETICS['hybrid']

def parse_lineage(lineage_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Parses raw lineage data into a structured JSON object for CultivarCreate.
    Extracts parent_1 and parent_2 names if available.
    """
    result = {
        'parent_1': None,
        'parent_2': None,
        'lineage_json': None
    }
    
    if not lineage_data or not isinstance(lineage_data, dict):
        return result
    
    # Store the raw lineage data
    result['lineage_json'] = lineage_data
    
    # Attempt to extract parent names from common API structures
    parents = lineage_data.get('parents', [])
    if isinstance(parents, list):
        if len(parents) >= 1:
            result['parent_1'] = parents[0].get('name') or parents[0].get('strain_name')
        if len(parents) >= 2:
            result['parent_2'] = parents[1].get('name') or parents[1].get('strain_name')
    
    # Clean up parent names (ensure they are strings and not empty)
    for key in ['parent_1', 'parent_2']:
        if result[key] and isinstance(result[key], str):
            result[key] = result[key].strip()
        else:
            result[key] = None
            
    return result

def map_cannabis_api_breeder(breeder_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Maps raw breeder data from The_Cannabis_API to a BreederCreate dictionary.
    """
    if not breeder_data or not isinstance(breeder_data, dict):
        return {}
    
    # BreederCreate fields: name, country, website, seedfinder_id, description
    
    mapped_data = {
        'name': breeder_data.get('name'),
        'country': normalize_country_code(breeder_data.get('country')),
        'website': validate_and_normalize_url(breeder_data.get('website')),
        'description': breeder_data.get('description'),
        # Assuming 'id' from the API can be used as an external ID reference
        'seedfinder_id': str(breeder_data.get('id')) if breeder_data.get('id') else None,
    }
    
    # Filter out None values for optional fields, but keep 'name' even if None (Pydantic will raise error)
    return {k: v for k, v in mapped_data.items() if v is not None}

def map_cannabis_api_strain(strain_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Maps raw strain data from The_Cannabis_API to a CultivarCreate dictionary.
    Avoids creating any 'strain' fields, using 'cultivar' terminology.
    """
    if not strain_data or not isinstance(strain_data, dict):
        return {}
    
    # CultivarCreate fields: name, indica, sativa, autoflower, parent_1, parent_2, lineage_json, 
    # seedfinder_id, thc_content, cbd_content, flowering_type, cycle_time, seed_count, url, description
    
    # 1. Genetics mapping
    race = strain_data.get('race')
    genetics = parse_race_to_genetics(race)
    
    # 2. Lineage parsing
    lineage_info = parse_lineage(strain_data.get('lineage'))
    
    # 3. Flowering type/Autoflower detection
    flowering_type = strain_data.get('flowering_type')
    autoflower = flowering_type and 'autoflower' in flowering_type.lower()
    
    # 4. THC/CBD content (API might use 'thc'/'cbd' or 'thc_content'/'cbd_content')
    thc_content = strain_data.get('thc_content') or strain_data.get('thc')
    cbd_content = strain_data.get('cbd_content') or strain_data.get('cbd')
    
    # 5. Description/URL
    description = strain_data.get('description')
    url = validate_and_normalize_url(strain_data.get('url'))
    
    mapped_data = {
        'name': strain_data.get('name'),
        'indica': genetics.get('indica', 0),
        'sativa': genetics.get('sativa', 0),
        'autoflower': autoflower,
        
        # Lineage fields
        'parent_1': lineage_info['parent_1'],
        'parent_2': lineage_info['parent_2'],
        'lineage_json': lineage_info['lineage_json'],
        
        # Other fields
        'flowering_type': flowering_type,
        'cycle_time': strain_data.get('cycle_time'),
        'seed_count': strain_data.get('seed_count'),
        'url': url,
        'description': description,
        
        # External ID (using API 'id' as external reference)
        'seedfinder_id': str(strain_data.get('id')) if strain_data.get('id') else None,
    }

    # Include cannabinoid keys only if the original API provided them (even if parsing yields None).
    # This preserves the presence of the key when the source had the field, while still allowing
    # absence when the source omitted the field entirely.
    if ('thc_content' in strain_data) or ('thc' in strain_data) or (thc_content is not None):
        mapped_data['thc_content'] = parse_percentage_value(thc_content)

    if ('cbd_content' in strain_data) or ('cbd' in strain_data) or (cbd_content is not None):
        mapped_data['cbd_content'] = parse_percentage_value(cbd_content)

    # Filter out None values for optional fields, but preserve cannabinoid keys if they were present
    return {
        k: v
        for k, v in mapped_data.items()
        if v is not None or k in ('thc_content', 'cbd_content')
    }