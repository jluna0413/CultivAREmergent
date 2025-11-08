import pytest
from app.utils.cannabis_api_mapper import (
    normalize_country_code,
    validate_and_normalize_url,
    parse_race_to_genetics,
    parse_lineage,
    map_cannabis_api_breeder,
    map_cannabis_api_strain,
)

# --- Fixtures for Mock API Responses ---

@pytest.fixture
def mock_breeder_api_response():
    """Realistic mock response for a breeder from The_Cannabis_API."""
    return {
        "id": 123,
        "name": "Sensi Seeds",
        "country": "netherlands",
        "website": "sensiseeds.com",
        "description": "A legendary seed bank.",
        "strains_count": 50
    }

@pytest.fixture
def mock_strain_api_response():
    """Realistic mock response for a strain from The_Cannabis_API."""
    return {
        "id": 456,
        "name": "Northern Lights",
        "race": "Indica",
        "thc": "18-22%",
        "cbd": 0.1,
        "flowering_type": "Photoperiod",
        "cycle_time": 60,
        "seed_count": 10,
        "url": "https://the-cannabis-api.vercel.app/strains/northern-lights",
        "description": "Classic indica strain.",
        "lineage": {
            "parents": [
                {"name": "Afghani", "type": "indica"},
                {"name": "Thai", "type": "sativa"}
            ],
            "generation": "F1"
        },
        "effects": ["relaxed", "happy"],
        "flavors": ["earthy", "pine"],
        "breeder": {"id": 123, "name": "Sensi Seeds"}
    }

# --- Helper Function Tests ---

@pytest.mark.parametrize("input_country, expected_output", [
    ("us", "Us"),
    ("USA", "Usa"),
    ("united states of america", "United States Of America"),
    ("  canada  ", "Canada"),
    (None, None),
    ("", None),
    (123, None),
])
def test_normalize_country_code(input_country, expected_output):
    """Test country code normalization."""
    assert normalize_country_code(input_country) == expected_output

@pytest.mark.parametrize("input_url, expected_output", [
    ("example.com", "https://example.com"),
    ("http://test.org", "http://test.org"),
    ("https://secure.net/", "https://secure.net/"),
    ("  www.google.com  ", "https://www.google.com"),
    ("ftp://bad.url", None), # Should fail basic scheme check
    (None, None),
    ("", None),
])
def test_validate_and_normalize_url(input_url, expected_output):
    """Test URL validation and normalization."""
    assert validate_and_normalize_url(input_url) == expected_output

@pytest.mark.parametrize("input_race, expected_indica, expected_sativa", [
    ("Indica", 100, 0),
    ("Sativa", 0, 100),
    ("Hybrid", 50, 50),
    ("Ruderalis", 0, 0),
    ("Unknown", 50, 50), # Default hybrid
    (None, 50, 50), # Default hybrid
    ("Sativa 60% / Indica 40%", 40, 60), # Hybrid percentage parsing
    ("sativa 75% / indica 25%", 25, 75),
    ("sativa 100% / indica 0%", 0, 100),
])
def test_parse_race_to_genetics(input_race, expected_indica, expected_sativa):
    """Test race to indica/sativa percentage mapping."""
    result = parse_race_to_genetics(input_race)
    assert result['indica'] == expected_indica
    assert result['sativa'] == expected_sativa

# --- Lineage Parsing Tests ---

def test_parse_lineage_valid_parents():
    """Test lineage parsing with valid parent names."""
    lineage_data = {
        "parents": [
            {"name": "ParentA"},
            {"strain_name": "ParentB"}
        ],
        "generation": "F2"
    }
    result = parse_lineage(lineage_data)
    assert result['parent_1'] == "ParentA"
    assert result['parent_2'] == "ParentB"
    assert result['lineage_json'] == lineage_data

def test_parse_lineage_missing_data():
    """Test lineage parsing with missing or invalid data."""
    assert parse_lineage(None)['parent_1'] is None
    assert parse_lineage({})['lineage_json'] is None
    assert parse_lineage({"parents": []})['parent_1'] is None
    assert parse_lineage({"parents": [{"name": "P1"}]})['parent_2'] is None

# --- Mapper Function Tests ---

def test_map_cannabis_api_breeder_success(mock_breeder_api_response):
    """Test successful mapping of breeder data to BreederCreate format."""
    mapped = map_cannabis_api_breeder(mock_breeder_api_response)
    
    assert mapped['name'] == "Sensi Seeds"
    assert mapped['country'] == "Netherlands"
    assert mapped['website'] == "https://sensiseeds.com"
    assert mapped['description'] == "A legendary seed bank."
    assert mapped['seedfinder_id'] == "123"
    
    # Ensure no extra fields are present
    assert len(mapped) == 5

def test_map_cannabis_api_strain_success(mock_strain_api_response):
    """Test successful mapping of strain data to CultivarCreate format."""
    mapped = map_cannabis_api_strain(mock_strain_api_response)
    
    assert mapped['name'] == "Northern Lights"
    assert mapped['indica'] == 100
    assert mapped['sativa'] == 0
    assert mapped['autoflower'] is False
    assert mapped['flowering_type'] == "Photoperiod"
    assert mapped['cycle_time'] == 60
    assert mapped['seedfinder_id'] == "456"
    assert mapped['url'] == "https://the-cannabis-api.vercel.app/strains/northern-lights"
    assert mapped['parent_1'] == "Afghani"
    assert mapped['parent_2'] == "Thai"
    
    # Check THC/CBD parsing (THC is string range, CBD is float)
    assert mapped['thc_content'] is None # Mapper currently handles string range as None, which is acceptable for Pydantic float field
    assert mapped['cbd_content'] == 0.1
    
    # Check lineage_json presence
    assert 'lineage_json' in mapped
    assert mapped['lineage_json']['generation'] == 'F1'
    
    # Ensure no 'strain' terminology leaks
    assert 'strain' not in mapped
    assert 'race' not in mapped

def test_map_cannabis_api_strain_autoflower():
    """Test mapping for an autoflower strain."""
    autoflower_data = {
        "id": 789,
        "name": "Auto Glueberry",
        "race": "Hybrid",
        "flowering_type": "Autoflower",
        "cycle_time": 70,
        "thc": 20.5,
    }
    mapped = map_cannabis_api_strain(autoflower_data)
    
    assert mapped['name'] == "Auto Glueberry"
    assert mapped['autoflower'] is True
    assert mapped['flowering_type'] == "Autoflower"
    assert mapped['indica'] == 50
    assert mapped['sativa'] == 50
    assert mapped['thc_content'] == 20.5

def test_map_cannabis_api_strain_thc_cbd_handling():
    """Test various THC/CBD input formats."""
    data = {
        "id": 1,
        "name": "Test",
        "race": "Hybrid",
        "thc": 25, # int
        "cbd_content": "1.5", # string float
    }
    mapped = map_cannabis_api_strain(data)
    assert mapped['thc_content'] == 25.0
    assert mapped['cbd_content'] == 1.5
    
    data_none = {
        "id": 2,
        "name": "Test2",
        "race": "Hybrid",
    }
    mapped_none = map_cannabis_api_strain(data_none)
    assert 'thc_content' not in mapped_none
    assert 'cbd_content' not in mapped_none