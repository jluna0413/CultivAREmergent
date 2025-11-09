import pytest

from app.utils.cannabis_api_mapper import (
    normalize_country_code,
    validate_and_normalize_url,
    parse_race_to_genetics,
    parse_lineage,
    map_cannabis_api_breeder,
    map_cannabis_api_strain,
)


@pytest.fixture
def breeder_response():
    return {
        "id": 123,
        "name": "Example Breeder",
        "country": "us",
        "website": "examplebreeder.com",
        "description": "<p>Leading breeder of example cultivars</p>",
        "seedfinder_id": 999,
    }


@pytest.fixture
def strain_response():
    return {
        "id": 987,
        "name": "Example Kush",
        "race": "60% sativa",
        "lineage": "ParentA x ParentB",
        "thc": "18%",
        "cbd": "0.5%",
        "url": "www.examplestrain.info",
        "description": "<script>alert('x')</script><p>Nice aroma</p>",
        "seedfinder_id": 555,
    }


@pytest.mark.parametrize(
    "input_country,expected",
    [
        ("us", "US"),
        ("Us", "US"),
        ("united states", "United States"),
        ("", None),
        (None, None),
    ],
)
def test_normalize_country_code(input_country, expected):
    assert normalize_country_code(input_country) == expected


@pytest.mark.parametrize(
    "input_url,expected_prefix",
    [
        ("https://example.com", "https://example.com"),
        ("http://example.com/path", "http://example.com/path"),
        ("example.com", "https://example.com"),
        ("    example.org  ", "https://example.org"),
        ("not a url", None),
        (None, None),
    ],
)
def test_validate_and_normalize_url(input_url, expected_prefix):
    val = validate_and_normalize_url(input_url)
    if expected_prefix is None:
        assert val is None
    else:
        # guard against None from validator before calling string methods
        assert val is not None and val.lower().startswith(expected_prefix.lower())


@pytest.mark.parametrize(
    "race,exp_ind,exp_sat,exp_auto,exp_flower",
    [
        ("Sativa", 20, 80, False, None),
        ("Indica", 80, 20, False, None),
        ("50/50", 50, 50, False, None),
        ("60% sativa", 40, 60, False, None),
        ("auto sativa", 20, 80, True, "autoflower"),
        (None, 50, 50, False, None),
        ("hybrid", 50, 50, False, None),
        ("70-30", 30, 70, False, None),
    ],
)
def test_parse_race_to_genetics(race, exp_ind, exp_sat, exp_auto, exp_flower):
    ind, sat, autoflower, flowering_type = parse_race_to_genetics(race)
    assert int(ind) == int(exp_ind)
    assert int(sat) == int(exp_sat)
    assert bool(autoflower) == bool(exp_auto)
    assert flowering_type == exp_flower


@pytest.mark.parametrize(
    "lineage_input,exp_p1,exp_p2,exp_json",
    [
        ("ParentA x ParentB", "ParentA", "ParentB", {"lineage_text": "ParentA x ParentB"}),
        ("ParentA/ParentB", "ParentA", "ParentB", {"lineage_text": "ParentA/ParentB"}),
        ("SingleParent", "SingleParent", None, {"lineage_text": "SingleParent"}),
        ({"parent_1": "A", "parent_2": "B"}, "A", "B", {"parent_1": "A", "parent_2": "B"}),
        (None, None, None, None),
    ],
)
def test_parse_lineage(lineage_input, exp_p1, exp_p2, exp_json):
    p1, p2, json_val = parse_lineage(lineage_input)
    assert p1 == exp_p1
    assert p2 == exp_p2
    assert json_val == exp_json


def test_map_cannabis_api_breeder(breeder_response):
    mapped = map_cannabis_api_breeder(breeder_response)
    # Required keys for BreederCreate-like dict
    assert mapped.get("name") == "Example Breeder"
    assert mapped.get("country") == "US"
    # ensure website is present and normalized before asserting prefix
    assert mapped.get("website") and mapped.get("website").startswith("https://examplebreeder.com")
    assert "description" in mapped and "Leading breeder" in mapped["description"]
    assert mapped.get("seedfinder_id") == 999


def test_map_cannabis_api_breeder_missing_name():
    # Should return empty dict when no name present
    assert map_cannabis_api_breeder({}) == {}
    assert map_cannabis_api_breeder({"website": "x.com"}) == {}


def test_map_cannabis_api_strain(strain_response):
    mapped = map_cannabis_api_strain(strain_response, breeder_id=42, created_by=7)
    # Terminology must use 'cultivar' semantics (no 'strain' keys)
    assert "strain" not in mapped
    assert mapped.get("name") == "Example Kush"
    assert mapped.get("breeder_id") == 42
    assert isinstance(mapped.get("indica"), int)
    assert isinstance(mapped.get("sativa"), int)
    assert mapped.get("autoflower") in (True, False)
    assert mapped.get("parent_1") == "ParentA"
    assert mapped.get("parent_2") == "ParentB"
    assert mapped.get("lineage_json") == {"lineage_text": "ParentA x ParentB"}
    assert mapped.get("thc_content") == pytest.approx(18.0, rel=1e-3)
    assert mapped.get("cbd_content") == pytest.approx(0.5, rel=1e-3)
    assert mapped.get("created_by") == 7


def test_map_cannabis_api_strain_invalid_input():
    assert map_cannabis_api_strain({}) == {}
    assert map_cannabis_api_strain(None) == {}