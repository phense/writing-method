#!/usr/bin/env python3
"""Refuse the delivery gate until every check still was inspected.

Reads <stills dir>/stills.json, written by tools/stills.mjs. Every narration
line of the current timeline needs a still that is marked "inspected": true
and has no open finding.

Usage: python3 tools/check_review.py [stills]
Exit 1 names each still that is missing, not inspected or carries a finding.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import project  # noqa: E402


def check(timeline: dict, stills: list[dict]) -> list[str]:
    """Problems that keep gate 2 open; empty when every still was inspected."""
    by_file = {s["file"]: s for s in stills}
    problems = []
    if timeline.get("draft"):
        problems.append("the timeline is a draft: stills must show the voiced timing")
    for scene in timeline["scenes"]:
        for index in range(len(scene["lines"])):
            name = f"{scene['key']}-{index:02d}.png"
            still = by_file.get(name)
            if still is None:
                problems.append(f"{name}: no still rendered")
            elif still.get("inspected") is not True:
                problems.append(f"{name}: not inspected")
            elif still.get("finding"):
                problems.append(f"{name}: open finding: {still['finding']}")
    return problems


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    root = project.ROOT
    folder = Path(argv[0]) if argv else root / "stills"
    timeline_path, list_path = root / "src" / "timeline.json", folder / "stills.json"
    for path in (timeline_path, list_path):
        if not path.is_file():
            print(f"check_review: {path} is missing", file=sys.stderr)
            return 1
    problems = check(project.read_json(timeline_path), project.read_json(list_path))
    for problem in problems:
        print(problem)
    total = sum(len(s["lines"]) for s in project.read_json(timeline_path)["scenes"])
    print(f"{total - len([p for p in problems if '.png' in p])} of {total} stills inspected without finding")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
