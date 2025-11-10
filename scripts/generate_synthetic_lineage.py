"""Generate synthetic lineage data for LLM training using The_Cannabis_API.

Creates simple heuristic-derived parent pairs and lineage lists from mapped
cultivar records. Can source data from the CannabisApiService or from the
application DB (sync path). Outputs JSON or CSV.

Usage (CLI):
    python scripts/generate_synthetic_lineage.py --source cannabis_api --size 50 --format json
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ValidationError

try:
    from app.services.cannabis_api_service import CannabisApiService
except Exception:
    CannabisApiService = None  # type: ignore

logger = logging.getLogger("synthetic_lineage")
logging.basicConfig(level=logging.INFO)


class SyntheticRecord(BaseModel):
    cultivar: str
    parent_1: Optional[str] = None
    parent_2: Optional[str] = None
    lineage: List[str]


DEFAULT_TYPES = ["sativa", "indica", "hybrid"]


def derive_parents_from_cultivar(cultivar: Dict[str, Any]) -> Dict[str, Any]:
    """Derive parent_1/parent_2 and a lineage list from a cultivar dict.

    Behavior (priority):
    - Use structured `lineage_json` if present.
    - Use explicit `parent_1`/`parent_2` top-level keys if present.
    - Use effect/flavor/name heuristics to derive parents.
    - Use indica/sativa dominance (>60) to derive a parent label.
    - Return a dict {parent_1, parent_2, lineage} where lineage is a list.
    """
    # 0. Check structured lineage
    lineage_struct = cultivar.get("lineage_json") or cultivar.get("lineage")
    if isinstance(lineage_struct, dict):
        p1 = lineage_struct.get("parent_1") or lineage_struct.get("parent1")
        p2 = lineage_struct.get("parent_2") or lineage_struct.get("parent2")
        if p1 or p2:
            lineage_list = [p for p in (p1, p2) if p]
            return {"parent_1": p1, "parent_2": p2, "lineage": lineage_list}

    # 1. top-level explicit parents
    p1 = cultivar.get("parent_1")
    p2 = cultivar.get("parent_2")
    if p1 or p2:
        lineage_list = [p for p in (p1, p2) if p]
        return {"parent_1": p1, "parent_2": p2, "lineage": lineage_list}

    # normalize fields
    name = (cultivar.get("name") or "").lower()
    effects_field = cultivar.get("effects") or cultivar.get("effect")
    flavors_field = cultivar.get("flavors") or cultivar.get("flavour") or cultivar.get("taste")

    def to_list(val: Any) -> List[str]:
        if not val:
            return []
        if isinstance(val, str):
            return [p.strip().lower() for p in val.split(",") if p.strip()]
        if isinstance(val, list):
            return [str(p).strip().lower() for p in val if p]
        return []

    effects = to_list(effects_field)
    flavors = to_list(flavors_field)

    # mappings
    EFFECT_TO_PARENT = {
        "relaxed": "Afghan Indica",
        "sleepy": "Afghan Indica",
        "sedated": "Afghan Indica",
        "euphoric": "Haze Sativa",
        "energetic": "Haze Sativa",
        "uplifted": "Haze Sativa",
        "happy": "Haze Sativa",
    }
    for eff in effects:
        for k, v in EFFECT_TO_PARENT.items():
            if k in eff:
                lineage_list = [v]
                return {"parent_1": v, "parent_2": None, "lineage": lineage_list}

    FLAVOR_TO_PARENT = {
        "citrus": "Lemon",
        "lemon": "Lemon",
        "berry": "Blueberry",
        "blueberry": "Blueberry",
        "earth": "Northern Lights",
        "pine": "Pine Kush",
    }
    for f in flavors:
        for k, v in FLAVOR_TO_PARENT.items():
            if k in f:
                lineage_list = [v]
                return {"parent_1": v, "parent_2": None, "lineage": lineage_list}

    # name-based fallback
    if "berry" in name:
        return {"parent_1": "Blueberry", "parent_2": None, "lineage": ["Blueberry"]}

    # derive from indica/sativa dominance
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


def fetch_from_cannabis_api(service: CannabisApiService, size: int) -> List[Dict[str, Any]]:
    """Fetch cultivars from the cannabis API via service.search_cultivars_by_type
    iterating types until we collect `size` items or exhaust types.
    """
    results: List[Dict[str, Any]] = []
    for t in DEFAULT_TYPES:
        try:
            items = service.search_cultivars_by_type(t)
        except Exception:
            logger.exception("Error fetching from cannabis API for type %s", t)
            items = []
        for it in items:
            results.append(it)
            if len(results) >= size:
                return results[:size]
    # If still short, return what we have (caller may duplicate/randomize)
    return results[:size]


def generate_synthetic_lineage(source: str = "cannabis_api", size: int = 100, service: Optional[Any] = None) -> List[Dict[str, Any]]:
    """Main generator function used by CLI and tests.

    - source: 'cannabis_api' or 'db'
    - service: optional CannabisApiService instance (makes testing easier)
    """
    items: List[Dict[str, Any]] = []
    if source == "cannabis_api":
        if service is None:
            if CannabisApiService is None:
                raise RuntimeError("CannabisApiService not available in environment")
            service = CannabisApiService()
        items = fetch_from_cannabis_api(service, size)
    elif source == "db":
        # Attempt to import sync DB access patterns from populate_data style
        try:
            from app.models import Cultivar  # type: ignore
            from app import create_app, db  # type: ignore

            app = create_app()
            with app.app_context():
                records = db.session.query(Cultivar).limit(size).all()
                items = [r.__dict__ for r in records]
        except Exception:
            logger.exception("DB source not available; falling back to cannabis_api")
            if service is None:
                if CannabisApiService is None:
                    raise RuntimeError("CannabisApiService not available in environment")
                service = CannabisApiService()
            items = fetch_from_cannabis_api(service, size)
    else:
        raise ValueError("Unknown source: %s" % source)

    # Now derive synthetic records
    synthetic: List[Dict[str, Any]] = []
    for it in items:
        # Skip malformed items
        name = it.get("name")
        if not name:
            logger.warning("Skipping item with no name: %r", it)
            continue

        derived = derive_parents_from_cultivar(it)
        record = {
            "cultivar": name,
            "parent_1": derived.get("parent_1"),
            "parent_2": derived.get("parent_2"),
            "lineage": derived.get("lineage") or [],
        }

        # validate via Pydantic
        try:
            sr = SyntheticRecord(**record)
            synthetic.append(sr.model_dump())
        except ValidationError as e:
            logger.warning("Validation failed for %s: %s", name, e)
            continue

        if len(synthetic) >= size:
            break

    return synthetic


def write_output(records: List[Dict[str, Any]], fmt: str = "json", out_file: Optional[str] = None) -> None:
    if fmt == "json":
        text = json.dumps(records, indent=2)
        if out_file:
            with open(out_file, "w", encoding="utf-8") as fh:
                fh.write(text)
            logger.info("Wrote %d records to %s", len(records), out_file)
        else:
            print(text)
    elif fmt == "csv":
        fieldnames = ["cultivar", "parent_1", "parent_2", "lineage"]
        if out_file:
            fh = open(out_file, "w", newline="", encoding="utf-8")
        else:
            fh = sys.stdout
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            row = r.copy()
            row["lineage"] = json.dumps(row.get("lineage", []))
            writer.writerow(row)
        if out_file:
            fh.close()
    else:
        raise ValueError("Unsupported format: %s" % fmt)


def cli(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="generate_synthetic_lineage")
    parser.add_argument("--format", choices=("json", "csv"), default="json")
    parser.add_argument("--size", type=int, default=100)
    parser.add_argument("--source", choices=("cannabis_api", "db"), default="cannabis_api")
    parser.add_argument("--output-file", dest="output_file", default=None)
    args = parser.parse_args(argv)

    records = generate_synthetic_lineage(source=args.source, size=args.size)
    write_output(records, fmt=args.format, out_file=args.output_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
"""Generate synthetic lineage data for LLM training using The_Cannabis_API.

Creates simple heuristic-derived parent pairs and lineage lists from mapped
cultivar records. Can source data from the CannabisApiService or from the
application DB (sync path). Outputs JSON or CSV.

Usage (CLI):
    python scripts/generate_synthetic_lineage.py --source cannabis_api --size 50 --format json
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import random
import sys
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ValidationError

try:
    from app.services.cannabis_api_service import CannabisApiService
except Exception:
    CannabisApiService = None  # type: ignore

logger = logging.getLogger("synthetic_lineage")
logging.basicConfig(level=logging.INFO)


class SyntheticRecord(BaseModel):
    cultivar: str
    parent_1: Optional[str] = None
    parent_2: Optional[str] = None
    lineage: List[str]


DEFAULT_TYPES = ["sativa", "indica", "hybrid"]


def derive_parents_from_cultivar(cultivar: Dict[str, Any]) -> Dict[str, Any]:
    """Derive parent_1/parent_2 and a lineage list from a cultivar dict.

    Behavior (priority):
    - Use structured `lineage_json` if present.
    - Use explicit `parent_1`/`parent_2` top-level keys if present.
    - Use effect/flavor/name heuristics to derive parents.
    - Use indica/sativa dominance (>60) to derive a parent label.
    - Return a dict {parent_1, parent_2, lineage} where lineage is a list.
    """
    # 0. Check structured lineage
    lineage_struct = cultivar.get("lineage_json") or cultivar.get("lineage")
    if isinstance(lineage_struct, dict):
        p1 = lineage_struct.get("parent_1") or lineage_struct.get("parent1")
        p2 = lineage_struct.get("parent_2") or lineage_struct.get("parent2")
        if p1 or p2:
            lineage_list = [p for p in (p1, p2) if p]
            return {"parent_1": p1, "parent_2": p2, "lineage": lineage_list}

    # 1. top-level explicit parents
    p1 = cultivar.get("parent_1")
    p2 = cultivar.get("parent_2")
    if p1 or p2:
        lineage_list = [p for p in (p1, p2) if p]
        return {"parent_1": p1, "parent_2": p2, "lineage": lineage_list}

    # normalize fields
    name = (cultivar.get("name") or "").lower()
    effects_field = cultivar.get("effects") or cultivar.get("effect")
    flavors_field = cultivar.get("flavors") or cultivar.get("flavour") or cultivar.get("taste")

    def to_list(val: Any) -> List[str]:
        if not val:
            return []
        if isinstance(val, str):
            return [p.strip().lower() for p in val.split(",") if p.strip()]
        if isinstance(val, list):
            return [str(p).strip().lower() for p in val if p]
        return []

    effects = to_list(effects_field)
    flavors = to_list(flavors_field)

    # mappings
    EFFECT_TO_PARENT = {
        "relaxed": "Afghan Indica",
        "sleepy": "Afghan Indica",
        "sedated": "Afghan Indica",
        "euphoric": "Haze Sativa",
        "energetic": "Haze Sativa",
        "uplifted": "Haze Sativa",
        "happy": "Haze Sativa",
    }
    for eff in effects:
        for k, v in EFFECT_TO_PARENT.items():
            if k in eff:
                lineage_list = [v]
                return {"parent_1": v, "parent_2": None, "lineage": lineage_list}

    FLAVOR_TO_PARENT = {
        "citrus": "Lemon",
        "lemon": "Lemon",
        "berry": "Blueberry",
        "blueberry": "Blueberry",
        "earth": "Northern Lights",
        "pine": "Pine Kush",
    }
    for f in flavors:
        for k, v in FLAVOR_TO_PARENT.items():
            if k in f:
                lineage_list = [v]
                return {"parent_1": v, "parent_2": None, "lineage": lineage_list}

    # name-based fallback
    if "berry" in name:
        return {"parent_1": "Blueberry", "parent_2": None, "lineage": ["Blueberry"]}

    # derive from indica/sativa dominance
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
"""Generate synthetic lineage data for LLM training using The_Cannabis_API.

Creates simple heuristic-derived parent pairs and lineage lists from mapped
cultivar records. Can source data from the CannabisApiService or from the
application DB (sync path). Outputs JSON or CSV.

Usage (CLI):
    python scripts/generate_synthetic_lineage.py --source cannabis_api --size 50 --format json --output-file out.json
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import random
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ValidationError

try:
    from app.services.cannabis_api_service import CannabisApiService
except Exception:
    CannabisApiService = None  # type: ignore

logger = logging.getLogger("synthetic_lineage")
logging.basicConfig(level=logging.INFO)


class SyntheticRecord(BaseModel):
    cultivar: str
    parent_1: Optional[str] = None
    parent_2: Optional[str] = None
    lineage: List[str]


DEFAULT_TYPES = ["sativa", "indica", "hybrid"]


def derive_parents_from_cultivar(cultivar: Dict[str, Any]) -> Dict[str, Any]:
    """Apply simple heuristics to produce parent_1, parent_2, and lineage list.

    Heuristics (simple and extensible):
    - If `parent_1`/`parent_2` already present from mapper, use them.
    - Else, derive parent_1 based on indica/sativa dominance (>60% threshold).
    - If cultivar name contains 'berry', set parent_2='Blueberry'.
    - Make lineage a list of non-null parents plus derived traits.
    """
        """Derive parent_1 and parent_2 from a cultivar dict using simple heuristics.

        Heuristics (priority order):
        1. If cultivar contains explicit `lineage_json` with parent_1/parent_2 use them.
        2. If cultivar contains explicit `parent_1`/`parent_2` keys use them.
        3. If `effects` are present, map common effect keywords to known parents.
        4. If `flavors` (or `taste`/`flavour`) are present, map flavor keywords to likely parents.
        5. If cultivar name contains known keywords (e.g., 'berry'), use name-based parents.
        6. Fallback to (None, None).

        Returns a tuple (parent_1, parent_2) where each may be None.
        """
        # 0. lineage_json (explicit structured lineage)
        lineage = cultivar.get("lineage_json") or cultivar.get("lineage")
        if isinstance(lineage, dict):
            p1 = lineage.get("parent_1") or lineage.get("parent1")
            p2 = lineage.get("parent_2") or lineage.get("parent2")
            if p1 or p2:
                return p1, p2

        # 1. explicit parent_1/parent_2 keys on the top-level
        if cultivar.get("parent_1") or cultivar.get("parent_2"):
            return cultivar.get("parent_1"), cultivar.get("parent_2")

        # prepare normalized text fields
        name = (cultivar.get("name") or "").lower()
        effects_field = cultivar.get("effects") or cultivar.get("effect")
        flavors_field = cultivar.get("flavors") or cultivar.get("flavour") or cultivar.get("taste")

        def to_list(val: Any) -> list:
            if not val:
                return []
            if isinstance(val, str):
                # split on commas
                return [p.strip().lower() for p in val.split(",") if p.strip()]
            if isinstance(val, list):
                return [str(p).strip().lower() for p in val if p]
            return []

        effects = to_list(effects_field)
        flavors = to_list(flavors_field)

        # 2. effect -> parent mapping (simple)
        EFFECT_TO_PARENT = {
            "relaxed": "Afghan Indica",
            "sleepy": "Afghan Indica",
            "sedated": "Afghan Indica",
            "euphoric": "Haze Sativa",
            "energetic": "Haze Sativa",
            "uplifted": "Haze Sativa",
            "happy": "Haze Sativa",
        }

        for eff in effects:
            for k, v in EFFECT_TO_PARENT.items():
                if k in eff:
                    return v, None

        # 3. flavor -> parent mapping
        FLAVOR_TO_PARENT = {
            "citrus": "Lemon",
            "lemon": "Lemon",
            "berry": "Blueberry",
            "blueberry": "Blueberry",
            "earth": "Northern Lights",
            "pine": "Pine Kush",
        }
        for f in flavors:
            for k, v in FLAVOR_TO_PARENT.items():
                if k in f:
                    return v, None

        # 4. name-based fallback heuristics
        if "berry" in name:
            return "Blueberry", None

        # 5. final fallback
        return None, None

    # Use existing parents if present
    if p1 or p2:
        lineage = [p for p in [p1, p2] if p]
        return {"parent_1": p1, "parent_2": p2, "lineage": lineage}

    indica = cultivar.get("indica")
    sativa = cultivar.get("sativa")

    derived_p1 = None
    if isinstance(indica, (int, float)) and indica >= 60:
        derived_p1 = "Indica-dominant"
    elif isinstance(sativa, (int, float)) and sativa >= 60:
        derived_p1 = "Sativa-dominant"

    derived_p2 = None
    if "berry" in name.lower():
        derived_p2 = "Blueberry"

    lineage = [x for x in (derived_p1, derived_p2) if x]

    # If no derived parents, add a generic marker
    if not lineage:
        lineage = ["Unknown-heritage"]

    return {"parent_1": derived_p1, "parent_2": derived_p2, "lineage": lineage}


def fetch_from_cannabis_api(service: CannabisApiService, size: int) -> List[Dict[str, Any]]:
    """Fetch cultivars from the cannabis API via service.search_cultivars_by_type
    iterating types until we collect `size` items or exhaust types.
    """
    results: List[Dict[str, Any]] = []
    for t in DEFAULT_TYPES:
        try:
            items = service.search_cultivars_by_type(t)
        except Exception:
            logger.exception("Error fetching from cannabis API for type %s", t)
            items = []
        for it in items:
            results.append(it)
            if len(results) >= size:
                return results[:size]
    # If still short, return what we have (caller may duplicate/randomize)
    return results[:size]


def generate_synthetic_lineage(source: str = "cannabis_api", size: int = 100, service: Optional[Any] = None) -> List[Dict[str, Any]]:
    """Main generator function used by CLI and tests.

    - source: 'cannabis_api' or 'db'
    - service: optional CannabisApiService instance (makes testing easier)
    """
    items: List[Dict[str, Any]] = []
    if source == "cannabis_api":
        if service is None:
            if CannabisApiService is None:
                raise RuntimeError("CannabisApiService not available in environment")
            service = CannabisApiService()
        items = fetch_from_cannabis_api(service, size)
    elif source == "db":
        # Attempt to import sync DB access patterns from populate_data style
        try:
            from app.models import Cultivar  # type: ignore
            from app import create_app, db  # type: ignore

            app = create_app()
            with app.app_context():
                records = db.session.query(Cultivar).limit(size).all()
                items = [r.__dict__ for r in records]
        except Exception:
            logger.exception("DB source not available; falling back to cannabis_api")
            if service is None:
                if CannabisApiService is None:
                    raise RuntimeError("CannabisApiService not available in environment")
                service = CannabisApiService()
            items = fetch_from_cannabis_api(service, size)
    else:
        raise ValueError("Unknown source: %s" % source)

    # Now derive synthetic records
    synthetic: List[Dict[str, Any]] = []
    for it in items:
        # Skip malformed items
        name = it.get("name")
        if not name:
            logger.warning("Skipping item with no name: %r", it)
            continue

        derived = derive_parents_from_cultivar(it)
        record = {
            "cultivar": name,
            "parent_1": derived.get("parent_1"),
            "parent_2": derived.get("parent_2"),
            "lineage": derived.get("lineage") or [],
        }

        # validate via Pydantic
        try:
            sr = SyntheticRecord(**record)
            synthetic.append(sr.model_dump())
        except ValidationError as e:
            logger.warning("Validation failed for %s: %s", name, e)
            continue

        if len(synthetic) >= size:
            break

    return synthetic


def write_output(records: List[Dict[str, Any]], fmt: str = "json", out_file: Optional[str] = None) -> None:
    if fmt == "json":
        text = json.dumps(records, indent=2)
        if out_file:
            with open(out_file, "w", encoding="utf-8") as fh:
                fh.write(text)
        else:
            print(text)
    elif fmt == "csv":
        fieldnames = ["cultivar", "parent_1", "parent_2", "lineage"]
        if out_file:
            fh = open(out_file, "w", newline='', encoding="utf-8")
        else:
            import sys

            fh = sys.stdout
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            row = r.copy()
            row["lineage"] = json.dumps(row.get("lineage", []))
            writer.writerow(row)
        if out_file:
            fh.close()
    else:
        raise ValueError("Unsupported format: %s" % fmt)


def cli(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="generate_synthetic_lineage")
    parser.add_argument("--format", choices=("json", "csv"), default="json")
    parser.add_argument("--size", type=int, default=100)
    parser.add_argument("--source", choices=("cannabis_api", "db"), default="cannabis_api")
    parser.add_argument("--output-file", dest="output_file", default=None)
    args = parser.parse_args(argv)

    records = generate_synthetic_lineage(source=args.source, size=args.size)
    write_output(records, fmt=args.format, out_file=args.output_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
