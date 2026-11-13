#!/usr/bin/env python3
"""Spoken form of narration lines: pronunciation list and provider markup.

A pronunciation entry fixes how one term is spoken, everywhere:
  {"term": "Tresor", "ipa": "tʁeˈzoːɐ̯", "key": true}
  {"term": "IT", "speak": "I T"}
  {"term": "Commit", "lang": "en-US", "key": true}
`speak` is a respelling, `ipa` a phonetic notation, `lang` marks the language.
`key` terms are verified by read-back. The project-wide list
(`pronunciation.json` beside the profile) and the video's own list are merged.
"""
import hashlib
import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

FIELDS = {"term", "speak", "ipa", "lang", "key"}


class PronunciationError(ValueError):
    pass


def load_pronunciation(*paths: Path) -> list[dict]:
    """Merge lists; the same term with different values is an error."""
    merged: dict[str, dict] = {}
    for path in paths:
        if not path or not Path(path).is_file():
            continue
        for entry in json.loads(Path(path).read_text()):
            unknown = set(entry) - FIELDS
            if unknown or not entry.get("term"):
                raise PronunciationError(f"{path}: invalid entry {entry!r}")
            known = merged.get(entry["term"])
            if known is not None and known != entry:
                raise PronunciationError(f"conflicting entries for term {entry['term']!r}")
            merged[entry["term"]] = entry
    # longest first, so "Azure AI Speech" wins over "Azure"
    return sorted(merged.values(), key=lambda e: -len(e["term"]))


def _pattern(term: str) -> re.Pattern:
    return re.compile(r"(?<![\w])" + re.escape(term) + r"(?![\w])")


def base_text(line: dict) -> str:
    """Text to speak before the pronunciation list: `speak` wins over `text`;
    backticks only mark code in the caption."""
    return (line.get("speak") or line["text"]).replace("`", "")


def spoken_plain(line: dict, entries: list[dict]) -> str:
    """Plain spoken text: respellings applied (for providers without markup)."""
    text = base_text(line)
    for entry in entries:
        if entry.get("speak"):
            text = _pattern(entry["term"]).sub(entry["speak"], text)
    return text


def spoken_ssml(line: dict, entries: list[dict]) -> str:
    """SSML body: respelling, phonetic notation and language marks applied."""
    text = base_text(line)
    slots: list[str] = []

    def hold(markup: str) -> str:
        slots.append(markup)
        return f"\x00{len(slots) - 1}\x00"

    for entry in entries:
        term = entry["term"]
        if entry.get("ipa"):
            markup = f'<phoneme alphabet="ipa" ph="{escape(entry["ipa"], {chr(34): "&quot;"})}">{escape(term)}</phoneme>'
        elif entry.get("speak"):
            markup = escape(entry["speak"])
        elif entry.get("lang"):
            markup = f'<lang xml:lang="{entry["lang"]}">{escape(term)}</lang>'
        else:
            continue
        text = _pattern(term).sub(lambda _m, markup=markup: hold(markup), text)
    parts = re.split(r"\x00(\d+)\x00", text)
    return "".join(slots[int(p)] if i % 2 else escape(p) for i, p in enumerate(parts))


def text_hash(line: dict, entries: list[dict], prof: dict) -> str:
    """Identity of a voiced line: spoken content plus language, voice and settings."""
    speech = prof["speech"]
    payload = json.dumps([spoken_ssml(line, entries), prof["language"], speech["voice"], speech["settings"]],
                         sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode()).hexdigest()[:10]


def audio_name(scene: str, index: int, digest: str) -> str:
    return f"{scene}-{index:02d}-{digest}.mp3"


def scene_file(scene: str) -> re.Pattern:
    """Sound files of exactly this scene (not of a scene whose key merely starts the same)."""
    return re.compile(rf"{re.escape(scene)}-\d{{2}}-[0-9a-f]{{10}}\.mp3")


def contains_tokens(haystack: list[str], needle: list[str]) -> bool:
    """True when `needle` occurs in `haystack` as a run of whole tokens."""
    n = len(needle)
    return bool(n) and any(haystack[i:i + n] == needle for i in range(len(haystack) - n + 1))


def key_terms(entries: list[dict]) -> list[str]:
    return [e["term"] for e in entries if e.get("key")]


def norm(word: str) -> str:
    return re.sub(r"[^\w]", "", word.lower(), flags=re.UNICODE)


def tokens(text: str) -> list[str]:
    return [t for t in (norm(w) for w in text.replace("`", "").split()) if t]


def pronunciation_paths(root: Path, profile: dict) -> list[Path]:
    return [Path(profile["_path"]).parent / "pronunciation.json", root / "pronunciation.json"]
