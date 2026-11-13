#!/usr/bin/env python3
"""Measure the result instead of trusting settings or exit codes.

  pace    words per minute per scene from the voiced sound, against the profile
  file    resolution, frame rate, duration, loudness and peak of a rendered file
  pauses  silence between narration lines in a rendered file, against the timeline
  all     pace, then file and pauses for the given file

Writes out/measure.json. Exit 1 on any deviation.

Usage: python3 tools/measure.py pace
       python3 tools/measure.py all out/video.mp4 [--offset SECONDS]
"""
import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audio  # noqa: E402
import profile as profile_mod  # noqa: E402
import project  # noqa: E402


def pace(manifest: dict, prof: dict) -> list[dict]:
    """Words per minute of pure speech per scene (edge silence excluded)."""
    low, high = prof["pace_wpm"]
    rows = []
    for scene, sounds in manifest.items():
        speech_s = sum(s["duration"] - s.get("lead_silence", 0) - s.get("trail_silence", 0) for s in sounds)
        count = sum(s.get("words", 0) for s in sounds)
        wpm = count / speech_s * 60 if speech_s > 0 else 0.0
        # a scene of a few words says nothing about pace
        ok = count < 20 or low <= wpm <= high
        rows.append({"scene": scene, "words": count, "wpm": round(wpm, 1), "ok": ok})
    return rows


def file_check(props: dict, loud: dict, prof: dict, expected_duration: float | None) -> list[dict]:
    picture, target = prof["picture"], prof["loudness"]
    rows = [
        {"what": "resolution", "measured": f"{props['width']}x{props['height']}",
         "expected": f"{picture['width']}x{picture['height']}",
         "ok": (props["width"], props["height"]) == (picture["width"], picture["height"])},
        {"what": "frame rate", "measured": props["fps"], "expected": picture["fps"],
         "ok": abs(props["fps"] - picture["fps"]) < 0.01},
        {"what": "sound track", "measured": props["has_audio"], "expected": True, "ok": bool(props["has_audio"])},
        {"what": "loudness (LUFS)", "measured": loud["lufs"], "expected": f"{target['lufs']} ± {target['tolerance']}",
         "ok": abs(loud["lufs"] - target["lufs"]) <= target["tolerance"]},
        {"what": "true peak (dBTP)", "measured": loud["true_peak"],
         "expected": f"<= {target['true_peak_max']} (+ {target['peak_tolerance']})",
         "ok": loud["true_peak"] <= target["true_peak_max"] + target["peak_tolerance"]},
    ]
    if expected_duration is not None:
        rows.append({"what": "duration (s)", "measured": props["duration"], "expected": round(expected_duration, 2),
                     "ok": abs(props["duration"] - expected_duration) <= 0.5})
    return rows


def expected_pauses(timeline: dict, offset: float = 0.0) -> list[dict]:
    """Silent gap between consecutive lines of a scene, in file time."""
    out = []
    for scene in timeline["scenes"]:
        lines = scene["lines"]
        for i in range(len(lines) - 1):
            start = offset + scene["start"] + lines[i]["speech_end"]
            end = offset + scene["start"] + lines[i + 1]["speech_start"]
            out.append({"scene": scene["key"], "line": i, "start": round(start, 3), "end": round(end, 3),
                        "expected": round(end - start, 3)})
    return out


def pause_check(expected: list[dict], silences: list[tuple[float, float]], tolerance: float) -> list[dict]:
    """Match each expected gap with the detected silence that overlaps it most."""
    rows = []
    for gap in expected:
        best = 0.0, None
        for start, end in silences:
            overlap = min(end, gap["end"]) - max(start, gap["start"])
            if overlap > best[0]:
                best = overlap, (start, end)
        measured = round(best[1][1] - best[1][0], 3) if best[1] else 0.0
        ok = measured > 0 and abs(measured - gap["expected"]) <= tolerance
        rows.append({**gap, "measured": measured, "ok": ok})
    return rows


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("what", choices=["pace", "file", "pauses", "all"])
    parser.add_argument("video", nargs="?")
    parser.add_argument("--offset", type=float, default=0.0, help="seconds of opening sequence in front")
    args = parser.parse_args(argv)
    root = project.ROOT
    try:
        prof = profile_mod.load(root)
        report, failed = {}, False
        if args.what in ("pace", "all"):
            rows = pace(project.load_manifest(root), prof)
            report["pace"] = rows
            for r in rows:
                print(f"pace   {r['scene']:20s} {r['wpm']:6.1f} wpm  {'ok' if r['ok'] else 'OUT OF RANGE ' + str(prof['pace_wpm'])}")
            failed |= not all(r["ok"] for r in rows)
        if args.what in ("file", "pauses", "all"):
            if not args.video:
                parser.error("a video file is required")
            video = Path(args.video)
            timeline_path = root / "src" / "timeline.json"
            timeline = project.read_json(timeline_path) if timeline_path.is_file() else None
            if args.what in ("file", "all"):
                expected = timeline["total"] + args.offset if timeline else None
                rows = file_check(audio.video_properties(video), audio.loudness(video), prof, expected)
                report["file"] = rows
                for r in rows:
                    print(f"file   {r['what']:20s} {str(r['measured']):>12s}  expected {r['expected']}  {'ok' if r['ok'] else 'FAIL'}")
                failed |= not all(r["ok"] for r in rows)
            if args.what in ("pauses", "all"):
                if timeline is None:
                    raise FileNotFoundError("src/timeline.json is missing; run tools/timeline.py")
                rows = pause_check(expected_pauses(timeline, args.offset), audio.silences(video, min_len=0.2),
                                   prof["pause_tolerance"])
                report["pauses"] = rows
                bad = [r for r in rows if not r["ok"]]
                mean = sum(r["measured"] for r in rows) / len(rows) if rows else 0
                print(f"pauses {len(rows)} gaps, mean {mean:.2f} s, {len(bad)} outside ± {prof['pause_tolerance']} s")
                for r in bad[:10]:
                    print(f"       {r['scene']}:{r['line']} expected {r['expected']} s, measured {r['measured']} s")
                failed |= bool(bad)
    except (audio.ToolMissing, profile_mod.ProfileError, FileNotFoundError) as error:
        print(f"measure: {error}", file=sys.stderr)
        return 1
    except (ValueError, subprocess.CalledProcessError):
        # ffprobe or the loudness pass could not read the file: no sound track, or a partial file
        print(f"measure: {args.video} has no sound track or cannot be read", file=sys.stderr)
        print("FAILED")
        return 1
    report["passed"] = not failed
    project.write_json(root / "out" / "measure.json", report)
    print("PASSED" if not failed else "FAILED")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
