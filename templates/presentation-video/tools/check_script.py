#!/usr/bin/env python3
"""Check a script before any paid voicing.

Reads video.json, src/scenes.json, src/narration.json and script/script.md and
reports every violation with scene and line. Errors block voicing (exit 1);
warnings do not.

`"purpose": "story"` in video.json marks narrated fiction: the narration is an
accepted manuscript edition, so no source is required and sentence length is
the author's choice; the edition and the manuscript revisions must be named.

Usage: python3 tools/check_script.py [--json]
"""
import difflib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import profile as profile_mod  # noqa: E402
import project  # noqa: E402
import speech  # noqa: E402

SECRET_PATTERNS = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    (re.compile(r"(?i)\b(pass(wor[dt])?|kennwort|secret|token|api[_-]?key)\s*[:=]\s*\S{6,}"), "credential assignment"),
    (re.compile(r"\b[A-Za-z0-9+/_-]{32,}\b"), "long token-like string"),
]
ABBREVIATION = re.compile(r"\b[A-ZÄÖÜ]{2,6}\b")
# digits a voice may read in an unintended way: times, versions, long numbers, units
NUMBER = re.compile(r"\b\d+[:./]\d+\b|\b\d{3,}\b|\b\d+\s?(%|[kMG]B|ms|min|s|h|px|€|\$)(?!\w)")
SCENE_KEY = re.compile(r"[a-z0-9_]+")
PURPOSES = ("tutorial", "story")
EDITIONS = ("verbatim", "listening")


def finding(severity, rule, message, scene=None, line=None):
    return {"severity": severity, "rule": rule, "scene": scene, "line": line, "message": message}


def source_ids(script_text: str) -> set[str]:
    return set(re.findall(r"^\|\s*(S\d+)\s*\|", script_text, re.M))


def section(script_text: str, title: str) -> str:
    match = re.search(rf"^##\s+{re.escape(title)}\s*\n(.*?)(?=^##\s|\Z)", script_text, re.M | re.S)
    return match.group(1).strip() if match else ""


def estimate_minutes(narration: dict, scenes: list[dict], prof: dict) -> float:
    total_words = sum(project.words(l["text"]) for ls in narration.values() for l in ls)
    lines = sum(len(ls) for ls in narration.values())
    pause = prof["pause"]
    speech_min = total_words / (sum(prof["pace_wpm"]) / 2)
    pause_min = (lines * pause["line"] + len(scenes) * (pause["scene_start"] + pause["scene_end"])) / 60
    return speech_min + pause_min


def split_proposal(narration: dict, scenes: list[dict]) -> str | None:
    """Chapter boundary closest to half of the words."""
    total = sum(project.words(l["text"]) for ls in narration.values() for l in ls)
    best, running, previous = None, 0, None
    for scene in scenes:
        chapter = scene.get("chapter")
        if previous is not None and chapter != previous:
            distance = abs(running - total / 2)
            if best is None or distance < best[0]:
                best = (distance, chapter)
        previous = chapter
        running += sum(project.words(l["text"]) for l in narration.get(scene["key"], []))
    return best[1] if best else None


def check(video: dict, scenes: list[dict], narration: dict, script_text: str,
          prof: dict, entries: list[dict]) -> list[dict]:
    out = []
    limits = prof["script"]
    purpose = video.get("purpose", "tutorial")
    if purpose not in PURPOSES:
        out.append(finding("error", "purpose", f"video.json purpose must be one of {', '.join(PURPOSES)}"))
    story = purpose == "story"
    if story:
        # the narration is a manuscript edition: name which one and what it was taken from
        if video.get("edition") not in EDITIONS:
            out.append(finding("error", "edition", f"a story video must name its edition: {' or '.join(EDITIONS)}"))
        based_on = video.get("based_on")
        if not (isinstance(based_on, list) and based_on and all(
                isinstance(b, dict) and b.get("chapter_id") and b.get("revision") for b in based_on)):
            out.append(finding("error", "based-on", "a story video must list the manuscript it narrates: based_on entries with chapter_id and revision"))

    # FR-001: one audience, one form of address
    if not isinstance(video.get("audience"), str):
        out.append(finding("error", "audience", "video.json must name exactly one audience (a second audience needs a second script)"))
    if not isinstance(video.get("address"), str):
        out.append(finding("error", "address", "video.json must name one form of address"))

    # FR-002: scenes with one message; narration and scene list agree
    keys = [s.get("key") for s in scenes]
    if len(keys) != len(set(keys)):
        out.append(finding("error", "scenes", "duplicate scene key in src/scenes.json"))
    for key in sorted(set(narration) - set(keys)):
        out.append(finding("error", "scenes", "narration has no entry in src/scenes.json", key))
    known_sources = source_ids(script_text)
    for scene in scenes:
        key = scene.get("key")
        for field in set(scene) - project.SCENE_FIELDS:
            out.append(finding("error", "scenes", f"unknown field {field!r}", key))
        if not SCENE_KEY.fullmatch(str(key)):
            out.append(finding("error", "scenes", "scene key may contain only lowercase letters, digits and _", key))
        if not scene.get("message"):
            out.append(finding("error", "message", "scene states no message", key))
        if not scene.get("chapter"):
            out.append(finding("error", "chapter", "scene belongs to no chapter", key))
        if key not in narration or not narration[key]:
            out.append(finding("error", "scenes", "scene has no narration", key))
        # FR-004: every claim traceable or marked; a story scene makes no claim
        cited = scene.get("sources") or []
        if not (story or cited or scene.get("unverified") or scene.get("no_claims")):
            out.append(finding("error", "sources", "scene cites no source and is not marked unverified or no_claims", key))
        for sid in cited:
            if sid not in known_sources:
                out.append(finding("error", "sources", f"source {sid} is not listed in script/script.md", key))
        if scene.get("unverified"):
            out.append(finding("warning", "sources", "scene is marked unverified", key))

    listed = {e["term"] for e in entries}
    for key, lines in narration.items():
        for i, line in enumerate(lines):
            for field in set(line) - project.LINE_FIELDS:
                out.append(finding("error", "line", f"unknown field {field!r}", key, i))
            text = line.get("text", "")
            if not text.strip():
                out.append(finding("error", "line", "empty narration line", key, i))
                continue
            # FR-003: written for listening
            count = project.words(text)
            if count > limits["max_line_words"]:
                out.append(finding("error", "line-length", f"{count} words, limit {limits['max_line_words']}", key, i))
            for sentence in re.split(r"(?<=[.!?])\s+", text):
                n = project.words(sentence)
                if n > limits["max_sentence_words"] and not story:
                    out.append(finding("warning", "sentence-length", f"sentence of {n} words, hard to follow by ear (limit {limits['max_sentence_words']})", key, i))
            if "speak" not in line:
                for abbr in sorted(set(ABBREVIATION.findall(text)) - listed):
                    out.append(finding("warning", "speakable", f"abbreviation {abbr!r} has no spoken form (pronunciation list or speak)", key, i))
                number = NUMBER.search(text)
                if number:
                    out.append(finding("warning", "speakable", f"number {number.group(0)!r} is not written the way it is spoken (add speak)", key, i))
            # FR-005: caption and speech may differ in spelling, never in meaning
            if line.get("speak"):
                ratio = difflib.SequenceMatcher(None, speech.tokens(text), speech.tokens(line["speak"]), autojunk=False).ratio()
                if ratio < 0.5:
                    out.append(finding("error", "caption-speech", f"caption and spoken form differ too much (similarity {ratio:.2f})", key, i))
            # FR-006: no secrets in narration
            for pattern, label in SECRET_PATTERNS:
                if pattern.search(text) or pattern.search(line.get("speak", "")):
                    out.append(finding("error", "secret", f"looks like a {label}", key, i))

    # FR-004: recreated interfaces need a notice and a written list
    if video.get("recreated"):
        early = [l for s in scenes[:2] for l in narration.get(s.get("key"), [])]
        if not any(l.get("notice") for l in early):
            out.append(finding("error", "notice", "interfaces are recreated: one line in the first two scenes must tell the viewer (\"notice\": true)"))
        evidence = section(script_text, "Evidenced, approximated, invented")
        if not evidence or "<" in evidence:
            out.append(finding("error", "evidence-list", "script/script.md must list what is evidenced, approximated and invented"))
    if not known_sources and not story:
        out.append(finding("error", "sources", "script/script.md lists no source (table rows S1, S2, ...)"))

    # FR-036: no length recommendation, one maximum
    minutes = estimate_minutes(narration, scenes, prof)
    if minutes > limits["max_minutes"]:
        at = split_proposal(narration, scenes)
        hint = f"; split before chapter {at!r}" if at else "; add chapters so it can be split"
        out.append(finding("error", "length", f"estimated {minutes:.0f} min exceeds the maximum of {limits['max_minutes']} min{hint}"))
    return out


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    root = project.ROOT
    try:
        prof = profile_mod.load(root)
        video = profile_mod.load_video(root)
        entries = speech.load_pronunciation(*speech.pronunciation_paths(root, prof))
    except (profile_mod.ProfileError, speech.PronunciationError) as error:
        print(f"check_script: {error}", file=sys.stderr)
        return 1
    scenes, narration = project.load_scenes(root), project.load_narration(root)
    script_path = root / "script" / "script.md"
    script_text = script_path.read_text() if script_path.is_file() else ""
    findings = check(video, scenes, narration, script_text, prof, entries)
    minutes = estimate_minutes(narration, scenes, prof)
    if "--json" in argv:
        print(json.dumps({"estimated_minutes": round(minutes, 1), "findings": findings}, indent=2, ensure_ascii=False))
    else:
        for f in findings:
            where = f["scene"] or "-"
            if f["line"] is not None:
                where += f":{f['line']}"
            print(f"{f['severity']:7s} {f['rule']:16s} {where:18s} {f['message']}")
        errors = sum(f["severity"] == "error" for f in findings)
        print(f"{errors} error(s), {len(findings) - errors} warning(s); estimated length {minutes:.1f} min")
    return 1 if any(f["severity"] == "error" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
