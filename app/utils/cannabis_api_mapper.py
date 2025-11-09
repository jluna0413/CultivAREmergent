"""Mapper utilities for The_Cannabis_API responses.
Produces dicts compatible with BreederCreate and CultivarCreate Pydantic models.
"""

import re
from typing import Any, Dict, Optional, Tuple

from app.utils import validators


def normalize_country_code(country: Optional[str]) -> Optional[str]:
    """
    Normalize country name or code to a short display string.
    If two-letter code provided, uppercase it; otherwise title-case the name.
    """
    if not country:
        return None
    c = country.strip()
    if len(c) == 2:
        return c.upper()
    return c.title()


def validate_and_normalize_url(url: Optional[str]) -> Optional[str]:
    """
    Ensure url is well-formed and includes scheme. Return None if invalid.
    """
    if not url:
        return None
    u = url.strip()
    # simple check
    if not re.match(r"^(https?://)", u, re.IGNORECASE):
        u = "https://" + u
    # basic domain check
    if re.match(r"^https?://[^\s/]+\.[^\s/]+", u):
        return u
    return None


def parse_race_to_genetics(race: Optional[str]) -> Tuple[int, int, bool, Optional[str]]:
    # Derives indica/sativa from API 'race' (e.g., 'sativa' → 20% indica, 80% sativa); sets flowering_type.
    """
    Convert a race string into indica/sativa percentages and autoflower flag.
    Returns (indica, sativa, autoflower, flowering_type)
    """
    if not race:
        return 50, 50, False, None
    r = race.strip().lower()
    autoflower = False
    flowering_type = None
    # detect autoflower
    if "auto" in r:
        autoflower = True
        flowering_type = "autoflower"
    if "sativa" in r and "indica" in r:
        # mixed race; try to parse proportions like "60% sativa"
        m = re.search(r"(\d{1,3})\s*%?\s*sativa", r)
        if m:
            s = int(m.group(1))
            s = max(0, min(100, s))
            i = max(0, 100 - s)
            return i, s, autoflower, flowering_type
        # fallback balanced
        return 50, 50, autoflower, flowering_type
    if "sativa" in r:
        # sativa-dominant heuristic
        return 20, 80, autoflower, flowering_type
    if "indica" in r:
        return 80, 20, autoflower, flowering_type
    # if race includes percentages separated like "70/30"
    m = re.match(r"(\d{1,3})\s*[/\-]\s*(\d{1,3})", r)
    if m:
        a = int(m.group(1))
        b = int(m.group(2))
        # assume a is sativa if word 'sativa' not present -- distribute proportionally
        total = a + b if (a + b) > 0 else 100
        s = round((a / total) * 100)
        i = 100 - s
        return i, s, autoflower, flowering_type
    return 50, 50, autoflower, flowering_type


def parse_lineage(
    lineage: Optional[Any],
) -> Tuple[Optional[str], Optional[str], Optional[Dict[str, Any]]]:
    # Parses API lineage string/array to parent_1/parent_2/lineage_json; handles 'x' or '/' separators.
    """
    Parse lineage information from the API.
    Returns (parent_1, parent_2, lineage_json)
    """
    if not lineage:
        return None, None, None
    # lineage might be a dict or a string
    if isinstance(lineage, dict):
        # try to extract parents from known keys
        parent_1 = (
            lineage.get("parent_1")
            or lineage.get("parent1")
            or lineage.get("first_parent")
        )
        parent_2 = (
            lineage.get("parent_2")
            or lineage.get("parent2")
            or lineage.get("second_parent")
        )
        return parent_1, parent_2, lineage
    if isinstance(lineage, str):
        text = lineage.strip()
        # common separator 'x' or 'X' or '/'
        parts = re.split(r"\s*[xX/]\s*", text)
        if len(parts) >= 2:
            p1 = parts[0].strip()
            p2 = parts[1].strip()
            return p1 or None, p2 or None, {"lineage_text": text}
        # fallback single parent
        return text, None, {"lineage_text": text}
    # unknown format
    return None, None, None


def map_cannabis_api_breeder(api_obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map a breeder record from The_Cannabis_API to BreederCreate-compatible dict.
    Expected keys in api_obj are best-effort and optional.
    """
    if not api_obj:
        return {}
    name = api_obj.get("name") or api_obj.get("title") or api_obj.get("breeder_name")
    if not name:
        return {}
    country = normalize_country_code(
        api_obj.get("country") or api_obj.get("country_code")
    )
    website = validate_and_normalize_url(api_obj.get("website") or api_obj.get("url"))
    description = validators.sanitize_text_field(
        api_obj.get("description") or api_obj.get("about") or ""
    )[0]
    seedfinder_id = api_obj.get("seedfinder_id") or api_obj.get("seedfinder") or None

    return {
        "name": name.strip(),
        "country": country,
        "website": website,
        "description": description or None,
        "seedfinder_id": seedfinder_id,
    }


# Maps The_Cannabis_API 'strain' data to project Cultivar dict; ensures no 'strain' terminology leaks.
def map_cannabis_api_strain(
    api_obj: Dict[str, Any],
    breeder_id: Optional[int] = None,
    created_by: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Map a strain record from The_Cannabis_API into a cultivar create dict.
    Uses cultivar terminology and avoids any 'strain' fields.
    """
    if not api_obj:
        return {}
    name = api_obj.get("name") or api_obj.get("title") or api_obj.get("strain_name")
    if not name:
        return {}
    # genetics / race
    race = api_obj.get("race") or api_obj.get("genetics") or api_obj.get("type")
    indica, sativa, autoflower, flowering_type = parse_race_to_genetics(race)

    # Prioritize explicit indica/sativa values if they exist
    if "indica" in api_obj:
        indica = api_obj["indica"]
    if "sativa" in api_obj:
        sativa = api_obj["sativa"]

    parent_1, parent_2, lineage_json = parse_lineage(
        api_obj.get("lineage") or api_obj.get("parents") or api_obj.get("cross")
    )

    # cannabinoid content
    def _parse_percent(val):
        try:
            if val is None:
                return None
            if isinstance(val, str) and "%" in val:
                return float(val.replace("%", "").strip())
            return float(val)
        except Exception:
            return None

    thc = (
        _parse_percent(api_obj.get("thc"))
        or _parse_percent(api_obj.get("thc_percent"))
        or _parse_percent(api_obj.get("thc_content"))
    )
    cbd = (
        _parse_percent(api_obj.get("cbd"))
        or _parse_percent(api_obj.get("cbd_percent"))
        or _parse_percent(api_obj.get("cbd_content"))
    )

    url = validate_and_normalize_url(
        api_obj.get("url") or api_obj.get("website") or api_obj.get("info_url")
    )
    description = validators.sanitize_text_field(
        api_obj.get("description") or api_obj.get("notes") or ""
    )[0]
    seedfinder_id = api_obj.get("seedfinder_id") or api_obj.get("seedfinder") or None

    return {
        "name": name.strip(),
        "breeder_id": breeder_id,
        "indica": int(indica),
        "sativa": int(sativa),
        "autoflower": bool(autoflower),
        "parent_1": parent_1,
        "parent_2": parent_2,
        "lineage_json": lineage_json,
        "seedfinder_id": seedfinder_id,
        "thc_content": thc,
        "cbd_content": cbd,
        "flowering_type": flowering_type,
        "url": url,
        "description": description or None,
        "created_by": created_by,
    }
