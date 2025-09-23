#!/usr/bin/env python3
"""
Generate patch suggestions (dry-run) for trivially-safe replacements:
 - onclick="history.back()" -> data-action="back"
 - onclick="someFunc()" (no Jinja tokens inside) -> data-action="someFunc"
This script DOES NOT apply changes. It writes .patch files to scripts/patches/
for review.
"""
import re
from pathlib import Path
import difflib

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = ROOT / "app" / "web" / "templates"
PATCH_DIR = Path(__file__).parent / "patches"
PATCH_DIR.mkdir(exist_ok=True)

simple_onclick_re = re.compile(r'onclick\s*=\s*"([^"]+)"')
jinja_re = re.compile(r'(\{\{|\{\%|\}\}|\%\})')


def transform_line(line):
    m = simple_onclick_re.search(line)
    if not m:
        return None
    body = m.group(1).strip()
    # skip if Jinja inside
    if jinja_re.search(body):
        return None
    # simple patterns
    if body in ("history.back()", "history.go(-1)"):
        return line.replace(m.group(0), 'data-action="back"')
    # function call without args: saveStrain()
    fn_call = re.match(r'^([A-Za-z0-9_]+)\(\s*\)\s*;?$', body)
    if fn_call:
        fn = fn_call.group(1)
        return line.replace(m.group(0), f'data-action="{fn}"')
    return None


def generate_patch(path: Path):
    text = path.read_text(errors="replace").splitlines(keepends=True)
    new = []
    changed = False
    for ln in text:
        new_ln = transform_line(ln)
        if new_ln is not None:
            new.append(new_ln)
            changed = True
        else:
            new.append(ln)
    if changed:
        diff = difflib.unified_diff(text, new, fromfile=str(path), tofile=str(path), lineterm="")
        patch_path = PATCH_DIR / (path.name + ".patch")
        patch_path.write_text("\n".join(diff))
        return patch_path
    return None


def main():
    templates = list(TEMPLATES_DIR.rglob("*.html"))
    patches = []
    for f in templates:
        p = generate_patch(f)
        if p:
            print("Suggested patch:", p)
            patches.append(p)
    if not patches:
        print("No trivial patches suggested.")
    else:
        print(f"Generated {len(patches)} patch files in {PATCH_DIR}")


if __name__ == "__main__":
    main()
