# Cannabis API Synthetic Lineage Integration

This document explains the synthetic lineage generation pipeline that uses
The_Cannabis_API via the project `CannabisApiService` to produce training
data for LLM models.

Usage
-----

Run the provided CLI:

```powershell
python scripts/generate_synthetic_lineage.py --source cannabis_api --size 10 --format json --output-file lineage.json
```

Options
 - `--source`: `cannabis_api` (default) or `db`.
 - `--size`: number of synthetic records to generate.
 - `--format`: `json` (default) or `csv`.
 - `--output-file`: optional file path. If omitted, JSON prints to stdout.

Heuristics
----------

The script uses simple, extensible heuristics to derive parent relationships:

- If `parent_1` or `parent_2` is present from the API mapper, those are used.
- If `indica >= 60` → `parent_1` = `Indica-dominant`.
- If `sativa >= 60` → `parent_1` = `Sativa-dominant`.
- If cultivar name contains `berry` → `parent_2` = `Blueberry`.
- If no parents can be derived, `lineage` contains `Unknown-heritage`.

Output Schema
-------------

Each record follows the Pydantic schema:

- `cultivar` (str): cultivar name
- `parent_1` (str | null)
- `parent_2` (str | null)
- `lineage` (list[str]): ordered list of parents/derived nodes

Notes & Caveats
---------------

- The heuristics are intentionally simple for early LLM training. Extend them as
  needed to incorporate flavors, effects, lineage text, or external DB joins.
- The script falls back to `cannabis_api` if `db` cannot be used in the current
  environment.
- Respect the service rate limits when generating very large datasets. The
  service has internal rate-limiting and caching, but the script will iterate
  over types and may hit external API limits.

Tests
-----

Unit tests are in `tests/unit/test_generate_synthetic_lineage.py`. They cover
the basic derivation heuristics, integration with a fake service, and output
writing to JSON/CSV.
