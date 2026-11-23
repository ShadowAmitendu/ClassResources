#!/usr/bin/env python3
"""Generate one JSON resource index for each BCA semester."""

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEMESTERS = ROOT / "bca" / "semesters"
DATA = ROOT / "bca" / "data"
CATEGORIES = ("syllabus", "notes", "assignments", "question-papers")


def scan(folder: Path):
    entries = []
    if not folder.is_dir():
        return entries

    items = sorted(
        folder.iterdir(),
        key=lambda path: (not path.is_dir(), path.name.lower()),
    )
    for path in items:
        if path.name.startswith("."):
            continue
        if path.is_dir():
            entries.append({
                "type": "dir",
                "name": path.name,
                "path": path.as_posix(),
                "children": scan(path),
            })
        elif path.is_file():
            relative = path.relative_to(ROOT).as_posix()
            entries.append({
                "type": "file",
                "name": path.name,
                "path": relative,
                "url": relative,
            })
    return entries


def generate():
    DATA.mkdir(parents=True, exist_ok=True)
    generated_names = set()
    for semester in SEMESTERS.iterdir():
        if not semester.is_dir():
            continue

        generated_names.add(semester.name)
        data = {"metadata": {"lastUpdated": datetime.now().strftime("%B %d, %Y")}}
        for category in CATEGORIES:
            data[category] = scan(semester / category)

        output = DATA / f"{semester.name}.json"
        output.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"Generated {output.relative_to(ROOT).as_posix()}")

    for stale in DATA.glob("*.json"):
        if stale.stem not in generated_names:
            stale.unlink()
            print(f"Removed stale {stale.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    generate()
