import json
from types import SimpleNamespace

from scripts.generate_synthetic_lineage_new import (
    derive_parents_from_cultivar,
    generate_synthetic_lineage,
    write_output,
)


class FakeService:
    def __init__(self, items):
        self._items = items

    def search_cultivars_by_type(self, t):
        # ignore type and return list
        return self._items


def test_derive_parents_from_cultivar_existing_parents():
    it = {"name": "A", "parent_1": "P1", "parent_2": "P2"}
    out = derive_parents_from_cultivar(it)
    assert out["parent_1"] == "P1"
    assert out["parent_2"] == "P2"


def test_derive_parents_from_cultivar_berry_and_sativa():
    it = {"name": "Berry Blast", "sativa": 80, "indica": 20}
    out = derive_parents_from_cultivar(it)
    assert out["parent_1"] == "Sativa-dominant"
    assert out["parent_2"] == "Blueberry"
    assert "Sativa-dominant" in out["lineage"]


def test_generate_synthetic_lineage_from_service(tmp_path):
    items = [{"name": "Blueberry Bliss", "indica": 30, "sativa": 70}]
    svc = FakeService(items)
    records = generate_synthetic_lineage(source="cannabis_api", size=1, service=svc)
    assert len(records) == 1
    r = records[0]
    assert r["cultivar"] == "Blueberry Bliss"
    assert "Blueberry" in r["lineage"]


def test_write_output_json_and_csv(tmp_path):
    records = [{"cultivar": "C1", "parent_1": None, "parent_2": None, "lineage": ["Unknown-heritage"]}]
    jfile = tmp_path / "out.json"
    write_output(records, fmt="json", out_file=str(jfile))
    content = json.loads(jfile.read_text(encoding="utf-8"))
    assert isinstance(content, list) and content[0]["cultivar"] == "C1"

    cfile = tmp_path / "out.csv"
    write_output(records, fmt="csv", out_file=str(cfile))
    csv_text = cfile.read_text(encoding="utf-8")
    assert "cultivar" in csv_text
