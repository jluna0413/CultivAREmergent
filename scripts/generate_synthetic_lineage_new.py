"""Generate synthetic lineage data (new, cleaned implementation).
This is a copy of the generator with extended heuristics. Tests will import
this version to avoid editing the existing file in-place.
"""
from typing import Any, Dict, List, Optional
import argparse
import csv
import json
import logging
import sys
from pydantic import BaseModel, ValidationError

logger = logging.getLogger("synthetic_lineage_new")
logging.basicConfig(level=logging.INFO)


class SyntheticRecord(BaseModel):
    cultivar: str
    parent_1: Optional[str] = None
    parent_2: Optional[str] = None
    lineage: List[str]


DEFAULT_TYPES = ["sativa", "indica", "hybrid"]


def derive_parents_from_cultivar(cultivar: Dict[str, Any]) -> Dict[str, Any]:
    lineage_struct = cultivar.get("lineage_json") or cultivar.get("lineage")
    if isinstance(lineage_struct, dict):
        p1 = lineage_struct.get("parent_1") or lineage_struct.get("parent1")
        p2 = lineage_struct.get("parent_2") or lineage_struct.get("parent2")
        if p1 or p2:
            lineage_list = [p for p in (p1, p2) if p]
            return {"parent_1": p1, "parent_2": p2, "lineage": lineage_list}

    p1 = cultivar.get("parent_1")
    p2 = cultivar.get("parent_2")
    if p1 or p2:
        lineage_list = [p for p in (p1, p2) if p]
        return {"parent_1": p1, "parent_2": p2, "lineage": lineage_list}

    name = (cultivar.get("name") or "").lower()
    def to_list(val: Any):
        if not val:
            return []
        if isinstance(val, str):
            return [p.strip().lower() for p in val.split(",") if p.strip()]
        if isinstance(val, list):
            return [str(p).strip().lower() for p in val if p]
        return []

    effects = to_list(cultivar.get("effects") or cultivar.get("effect"))
    flavors = to_list(cultivar.get("flavors") or cultivar.get("flavour") or cultivar.get("taste"))

    EFFECT_TO_PARENT = {"relaxed": "Afghan Indica", "sleepy": "Afghan Indica", "euphoric": "Haze Sativa", "energetic": "Haze Sativa"}
    for eff in effects:
        for k, v in EFFECT_TO_PARENT.items():
            if k in eff:
                return {"parent_1": v, "parent_2": None, "lineage": [v]}

    FLAVOR_TO_PARENT = {"citrus": "Lemon", "berry": "Blueberry", "earth": "Northern Lights"}
    for f in flavors:
        for k, v in FLAVOR_TO_PARENT.items():
            if k in f:
                return {"parent_1": v, "parent_2": None, "lineage": [v]}

    if "berry" in name:
        return {"parent_1": "Blueberry", "parent_2": None, "lineage": ["Blueberry"]}

    indica = cultivar.get("indica")
    sativa = cultivar.get("sativa")
    derived_p1 = None
    if isinstance(indica, (int, float)) and indica >= 60:
        derived_p1 = "Indica-dominant"
    elif isinstance(sativa, (int, float)) and sativa >= 60:
        derived_p1 = "Sativa-dominant"

    derived_p2 = None
    if "berry" in name:
        derived_p2 = "Blueberry"

    lineage = [x for x in (derived_p1, derived_p2) if x]
    if not lineage:
        lineage = ["Unknown-heritage"]

    return {"parent_1": derived_p1, "parent_2": derived_p2, "lineage": lineage}


def generate_synthetic_lineage(source: str = "cannabis_api", size: int = 100, service: Optional[Any] = None):
    # minimal service fallback for tests
    items = []
    if source == "cannabis_api":
        if service is None:
            raise RuntimeError("service required for tests")
        items = service.search_cultivars_by_type('sativa')
    elif source == "db":
        items = []
    else:
        raise ValueError("Unknown source")

    out = []
    for it in items[:size]:
        if not it.get('name'):
            continue
        d = derive_parents_from_cultivar(it)
        rec = {"cultivar": it.get('name'), "parent_1": d.get('parent_1'), "parent_2": d.get('parent_2'), "lineage": d.get('lineage')}
        try:
            sr = SyntheticRecord(**rec)
            out.append(sr.model_dump())
        except ValidationError:
            continue
    return out


def write_output(records: List[Dict[str, Any]], fmt: str = "json", out_file: Optional[str] = None):
    if fmt == 'json':
        text = json.dumps(records, indent=2)
        if out_file:
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(text)
        else:
            print(text)
    elif fmt == 'csv':
        fieldnames = ['cultivar','parent_1','parent_2','lineage']
        fh = open(out_file,'w',newline='',encoding='utf-8') if out_file else sys.stdout
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            row = r.copy()
            row['lineage'] = json.dumps(row.get('lineage',[]))
            writer.writerow(row)
        if out_file:
            fh.close()
    else:
        raise ValueError('Unsupported format')
