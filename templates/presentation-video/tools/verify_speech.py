#!/usr/bin/env python3
"""Read the voiced lines back with speech recognition and compare.

A multilingual voice can read a plain word of the target language as foreign.
This tool catches that: every key term of the pronunciation list must be
recognized where the caption contains it, and each line must match its text.

  --samples   print the lines to voice first: one per key term (scene:index),
              to be voiced with `voice_azure.py --only ...` and verified
              before the whole video is voiced
  (default)   verify all voiced lines; needs <audio>.words.json beside each
              sound file, written by the profile's `transcribe` command
              ([{"word", "start", "end"}, ...])

Usage: python3 tools/verify_speech.py [--samples] [--only scene:index,...]
Exit 1 if a key term is not recognized.
"""
import argparse
import difflib
import shlex
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import profile as profile_mod  # noqa: E402
import project  # noqa: E402
import speech  # noqa: E402
import voice_azure  # noqa: E402


def samples(narration: dict, terms: list[str]) -> dict:
    """First line containing each key term: real context beats a test phrase."""
    found = {}
    for term in terms:
        pattern = speech._pattern(term)
        for scene, lines in narration.items():
            hit = next((i for i, l in enumerate(lines) if pattern.search(l["text"])), None)
            if hit is not None:
                found[term] = (scene, hit)
                break
    return found


def verify_line(line: dict, heard_words: list[str], entries: list[dict], threshold: float) -> dict:
    """Compare what was heard with the caption text.

    A key term counts as heard when its tokens, or the tokens of its
    respelling, occur as whole words: "it" inside "mit" is not a match, and a
    term respelled "I T" may be recognized as either "IT" or "I T".
    """
    expected = speech.tokens(line["text"])
    heard = [t for word in heard_words for t in speech.tokens(word)]
    ratio = difflib.SequenceMatcher(None, expected, heard, autojunk=False).ratio() if expected else 1.0
    missing = []
    for entry in entries:
        if not entry.get("key") or not speech._pattern(entry["term"]).search(line["text"]):
            continue
        forms = [speech.tokens(entry["term"])]
        if entry.get("speak"):
            forms.append(speech.tokens(entry["speak"]))
        if not any(speech.contains_tokens(heard, form) for form in forms):
            missing.append(entry["term"])
    return {"ratio": round(ratio, 2), "missing_terms": missing, "ok": not missing and ratio >= threshold}


def words_file(sound: Path) -> Path:
    return sound.with_suffix(".words.json")


def transcribe(sound: Path, command: str | None) -> None:
    if words_file(sound).is_file():
        return
    if not command:
        raise FileNotFoundError(f"{words_file(sound).name} is missing and the profile names no transcribe command")
    # split first, then substitute: a path with spaces stays one argument
    subprocess.run([part.replace("{audio}", str(sound)) for part in shlex.split(command)], check=True)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--samples", action="store_true")
    parser.add_argument("--only")
    parser.add_argument("--threshold", type=float, default=0.8)
    args = parser.parse_args(argv)
    root = project.ROOT
    try:
        prof = profile_mod.load(root)
        entries = speech.load_pronunciation(*speech.pronunciation_paths(root, prof))
        narration = project.load_narration(root)
        terms = speech.key_terms(entries)
        if args.samples:
            found = samples(narration, terms)
            for term, (scene, index) in found.items():
                print(f"{scene}:{index}\t{term}")
            for term in sorted(set(terms) - set(found)):
                print(f"-\t{term} (not used in this script)")
            if found:
                print("voice them first: python3 tools/voice_azure.py --only "
                      + ",".join(sorted({f"{s}:{i}" for s, i in found.values()})))
            return 0
        only = None
        if args.only:
            only = voice_azure.parse_only(args.only)
        manifest = project.load_manifest(root)
        failed, checked = [], 0
        for scene, lines in narration.items():
            for i, line in enumerate(lines):
                if only is not None and (scene, i) not in only:
                    continue
                digest = speech.text_hash(line, entries, prof)
                sound = root / "public" / "audio" / speech.audio_name(scene, i, digest)
                if not sound.is_file():
                    listed = manifest.get(scene, [])
                    sound = root / "public" / listed[i]["file"] if i < len(listed) else sound
                if not sound.is_file():
                    raise FileNotFoundError(f"{scene}:{i} is not voiced yet")
                transcribe(sound, prof["transcribe"])
                heard = [w["word"] for w in project.read_json(words_file(sound))]
                result = verify_line(line, heard, entries, args.threshold)
                checked += 1
                if not result["ok"]:
                    failed.append((scene, i, result, " ".join(heard)))
    except (FileNotFoundError, subprocess.CalledProcessError, profile_mod.ProfileError, speech.PronunciationError,
            voice_azure.ProviderError) as error:
        print(f"verify_speech: {error}", file=sys.stderr)
        return 1
    for scene, i, result, heard in failed:
        reason = f"key term not recognized: {', '.join(result['missing_terms'])}" if result["missing_terms"] \
            else f"similarity {result['ratio']}"
        print(f"{scene}:{i}  {reason}\n    heard: {heard}")
    key_failures = [f for f in failed if f[2]["missing_terms"]]
    print(f"{checked} lines checked, {len(key_failures)} with an unrecognized key term, "
          f"{len(failed) - len(key_failures)} below similarity {args.threshold} (listen to these)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
