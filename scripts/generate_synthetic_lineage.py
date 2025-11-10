"""Generate synthetic lineage data for LLM training.

This module creates heuristic-based parent assignments and lineage lists from
cultivar records. Data can come from the CannabisApiService or via a database
query performed in the application context. The output can be serialized to
JSON or CSV via the CLI.
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import random
import sys
from typing import Any, Dict, Iterable, List, Optional

from pydantic import BaseModel, ValidationError

try:
    from app.services.cannabis_api_service import CannabisApiService
except Exception:  # pragma: no cover - optional dependency for tests
    CannabisApiService = None  # type: ignore

logger = logging.getLogger("synthetic_lineage")
logging.basicConfig(level=logging.INFO)


class SyntheticRecord(BaseModel):
    cultivar: str
    parent_1: Optional[str] = None
    parent_2: Optional[str] = None
    lineage: List[str]


DEFAULT_TYPES: tuple[str, ...] = ("sativa", "indica", "hybrid")
EFFECT_PARENT_MAP = {
    "relaxed": "Afghan Indica",
    "sleepy": "Afghan Indica",
    "sedated": "Afghan Indica",
    "euphoric": "Haze Sativa",
    "energetic": "Haze Sativa",
    "uplifted": "Haze Sativa",
    "happy": "Haze Sativa",
}
FLAVOR_PARENT_MAP = {
    "citrus": "Lemon",
    "lemon": "Lemon",
    "berry": "Blueberry",
    "blueberry": "Blueberry",
    "earth": "Northern Lights",
    "pine": "Pine Kush",
}


def _normalize_list(value: Any) -> List[str]:
    if not value:
        return []
    if isinstance(value, str):
        return [part.strip().lower() for part in value.split(",") if part.strip()]
    if isinstance(value, Iterable):
        return [str(part).strip().lower() for part in value if part]
    return []


def derive_parents_from_cultivar(cultivar: Dict[str, Any]) -> Dict[str, Any]:
    """Derive parent fields and lineage values from a cultivar mapping."""

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
    effects = _normalize_list(cultivar.get("effects") or cultivar.get("effect"))
    flavors = _normalize_list(cultivar.get("flavors") or cultivar.get("flavour") or cultivar.get("taste"))

    for eff in effects:
        for key, parent in EFFECT_PARENT_MAP.items():
            if key in eff:
                return {"parent_1": parent, "parent_2": None, "lineage": [parent]}

    for flavor in flavors:
        for key, parent in FLAVOR_PARENT_MAP.items():
            if key in flavor:
                return {"parent_1": parent, "parent_2": None, "lineage": [parent]}

    indica_score = cultivar.get("indica")
    sativa_score = cultivar.get("sativa")
    derived_p1: Optional[str] = None
    if isinstance(indica_score, (int, float)) and indica_score >= 60:
        derived_p1 = "Indica-dominant"
    elif isinstance(sativa_score, (int, float)) and sativa_score >= 60:
        derived_p1 = "Sativa-dominant"

    derived_p2: Optional[str] = None
    if "berry" in name:
        derived_p2 = "Blueberry"

    lineage = [value for value in {derived_p1, derived_p2} if value]
    if not lineage:
        lineage = ["Unknown-heritage"]

    return {"parent_1": derived_p1, "parent_2": derived_p2, "lineage": lineage}


def fetch_from_cannabis_api(service: CannabisApiService, size: int) -> List[Dict[str, Any]]:
    """Collect cultivar entries from the API until *size* items are returned."""

    results: List[Dict[str, Any]] = []
    for cultivar_type in DEFAULT_TYPES:
        try:
            items = service.search_cultivars_by_type(cultivar_type)
        except Exception:  # pragma: no cover - defensive logging path
            logger.exception("Error fetching from cannabis API for type %s", cultivar_type)
            items = []
        results.extend(items)
        if len(results) >= size:
            break

    if len(results) > size:
        random.shuffle(results)
    return results[:size]


def generate_synthetic_lineage(
    source: str = "cannabis_api",
    size: int = 100,
    service: Optional[Any] = None,
) -> List[Dict[str, Any]]:
    """Build a synthetic lineage dataset for the given *source* and *size*."""

    items: List[Dict[str, Any]] = []
    if source == "cannabis_api":
        if service is None:
            if CannabisApiService is None:
                raise RuntimeError("CannabisApiService not available in environment")
            service = CannabisApiService()
        items = fetch_from_cannabis_api(service, size)
    elif source == "db":
        try:
            from app.models import Cultivar  # type: ignore
            from app import create_app, db  # type: ignore

            app = create_app()
            with app.app_context():
                records = db.session.query(Cultivar).limit(size).all()
                items = [record.__dict__ for record in records]
        except Exception:
            logger.exception("DB source unavailable; falling back to cannabis_api")
            if service is None:
                if CannabisApiService is None:
                    raise RuntimeError("CannabisApiService not available in environment")
                service = CannabisApiService()
            items = fetch_from_cannabis_api(service, size)
    else:
        raise ValueError(f"Unknown source: {source}")

    synthetic: List[Dict[str, Any]] = []
    for item in items:
        name = item.get("name")
        if not name:
            logger.warning("Skipping item with no name: %r", item)
            continue

        derived = derive_parents_from_cultivar(item)
        record = {
            "cultivar": name,
            "parent_1": derived.get("parent_1"),
            "parent_2": derived.get("parent_2"),
            "lineage": list(derived.get("lineage") or []),
        }

        try:
            model = SyntheticRecord(**record)
        except ValidationError as exc:
            logger.warning("Validation failed for %s: %s", name, exc)
            continue
        synthetic.append(model.model_dump())

        if len(synthetic) >= size:
            break

    return synthetic


def write_output(records: List[Dict[str, Any]], fmt: str = "json", out_file: Optional[str] = None) -> None:
    """Serialize records to JSON or CSV."""

    if fmt == "json":
        payload = json.dumps(records, indent=2)
        if out_file:
            with open(out_file, "w", encoding="utf-8") as handle:
                handle.write(payload)
            logger.info("Wrote %d records to %s", len(records), out_file)
        else:
            print(payload)
        return

    if fmt == "csv":
        fieldnames = ["cultivar", "parent_1", "parent_2", "lineage"]
        handle = open(out_file, "w", newline="", encoding="utf-8") if out_file else sys.stdout
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            row = dict(record)
            row["lineage"] = json.dumps(row.get("lineage", []))
            writer.writerow(row)
        if out_file:
            handle.close()
        return

    raise ValueError(f"Unsupported format: {fmt}")


def cli(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="generate_synthetic_lineage")
    parser.add_argument("--format", choices=("json", "csv"), default="json")
    parser.add_argument("--size", type=int, default=100)
    parser.add_argument("--source", choices=("cannabis_api", "db"), default="cannabis_api")
    parser.add_argument("--output-file", dest="output_file", default=None)
    parser.add_argument("--shuffle", action="store_true", help="Randomize order before writing output")
    args = parser.parse_args(argv)

    records = generate_synthetic_lineage(source=args.source, size=args.size)
    if args.shuffle:
        random.shuffle(records)
    write_output(records, fmt=args.format, out_file=args.output_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
