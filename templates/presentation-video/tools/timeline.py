#!/usr/bin/env python3
"""Derive the timeline from the measured sound. No time is authored by hand.

The first sound of a line starts exactly `pause.line` after the last sound of
the previous line: silence inside the sound files is subtracted, so the
audible pause equals the profile value for every provider. A line may ask for
more room with `min` (seconds its picture needs).

Writes src/timeline.json (read by the composition, check stills and
measurements) and out/captions.vtt.

Usage: python3 tools/timeline.py [--caption-offset SECONDS]
"""
import argparse
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import profile as profile_mod  # noqa: E402
import project  # noqa: E402
import speech  # noqa: E402


class StaleManifest(RuntimeError):
    pass


def build(scenes: list[dict], narration: dict, manifest: dict, prof: dict, hashes: dict | None = None) -> dict:
    """Timeline for all scenes. `hashes` ({scene: [hash, ...]}) guards against
    sound that no longer matches the text."""
    pause, fps = prof["pause"], prof["picture"]["fps"]
    out_scenes, chapters, cursor_frames = [], [], 0
    for scene in scenes:
        key = scene["key"]
        lines, sounds = narration[key], manifest.get(key)
        if sounds is None or len(sounds) != len(lines):
            raise StaleManifest(f"{key}: sound is missing or does not match the narration; voice it again")
        if hashes is not None:
            for i, sound in enumerate(sounds):
                if sound.get("hash") != hashes[key][i]:
                    raise StaleManifest(f"{key}:{i}: the text changed after voicing; voice it again")
        t = pause["scene_start"]
        timed = []
        for line, sound in zip(lines, sounds):
            lead, trail = sound.get("lead_silence", 0.0), sound.get("trail_silence", 0.0)
            audio_at = max(0.0, t - lead)
            speech_start = audio_at + lead
            speech_end = audio_at + sound["duration"] - trail
            at = max(0.0, speech_start - pause["caption_lead"])
            timed.append({"text": line["text"], "show": line.get("show", True), "min": line.get("min", 0),
                          "file": sound["file"], "at": at, "audio_at": audio_at,
                          "speech_start": speech_start, "speech_end": speech_end, "duration": sound["duration"]})
            t = max(speech_end + pause["line"], at + line.get("min", 0) + pause["caption_lead"])
        last = timed[-1]
        length = max(last["speech_end"] + pause["scene_end"], last["at"] + last["min"])
        for i, item in enumerate(timed):
            nxt = timed[i + 1]["at"] if i + 1 < len(timed) else length
            item["slot"] = nxt - item["at"]
            for field in ("at", "audio_at", "speech_start", "speech_end", "slot"):
                item[field] = round(item[field], 3)
            del item["min"]
        frames = math.ceil(length * fps)
        start = cursor_frames / fps
        if not chapters or chapters[-1]["title"] != scene.get("chapter"):
            chapters.append({"title": scene.get("chapter"), "start": round(start, 3)})
        out_scenes.append({"key": key, "chapter": scene.get("chapter"), "message": scene.get("message"),
                           "start": round(start, 3), "start_frame": cursor_frames,
                           "length": round(frames / fps, 3), "frames": frames, "lines": timed})
        cursor_frames += frames
    # the composition reads size and legibility limits from here, so the
    # profile is the single place they are set
    return {"fps": fps, "total": round(cursor_frames / fps, 3), "total_frames": cursor_frames,
            "picture": prof["picture"], "pause": pause, "chapters": chapters, "scenes": out_scenes}


def draft_manifest(narration: dict, prof: dict) -> dict:
    """Estimated sound for a preview before voicing: length from the word
    count at the middle of the pace range, no sound file."""
    wpm = sum(prof["pace_wpm"]) / 2
    return {scene: [{"file": None, "duration": round(max(0.6, project.words(l["text"]) / wpm * 60), 3),
                     "lead_silence": 0.0, "trail_silence": 0.0, "words": project.words(l["text"])} for l in lines]
            for scene, lines in narration.items()}


def _stamp(seconds: float) -> str:
    ms = round(seconds * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d}.{ms % 1000:03d}"


def captions(timeline: dict, offset: float = 0.0) -> str:
    """WebVTT from the same timeline, so subtitles cannot drift from speech."""
    cues = ["WEBVTT", ""]
    for scene in timeline["scenes"]:
        for line in scene["lines"]:
            if not line["show"]:
                continue
            start = offset + scene["start"] + line["at"]
            end = offset + scene["start"] + min(line["at"] + line["slot"], line["speech_end"] + 0.4)
            cues += [f"{_stamp(start)} --> {_stamp(end)}", line["text"].replace("`", ""), ""]
    return "\n".join(cues)


def chapter_list(timeline: dict, offset: float = 0.0) -> str:
    return "\n".join(f"{int((c['start'] + offset) // 60)}:{int((c['start'] + offset) % 60):02d} {c['title']}"
                     for c in timeline["chapters"])


def current_hashes(narration: dict, entries: list[dict], prof: dict) -> dict:
    return {scene: [speech.text_hash(l, entries, prof) for l in lines] for scene, lines in narration.items()}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--caption-offset", type=float, default=0.0,
                        help="seconds of opening sequence placed in front of the video")
    parser.add_argument("--draft", action="store_true",
                        help="estimate lengths without sound, to design the picture before voicing")
    args = parser.parse_args(argv)
    root = project.ROOT
    try:
        prof = profile_mod.load(root)
        entries = speech.load_pronunciation(*speech.pronunciation_paths(root, prof))
        narration = project.load_narration(root)
        if args.draft:
            timeline = build(project.load_scenes(root), narration, draft_manifest(narration, prof), prof)
            timeline["draft"] = True
        else:
            timeline = build(project.load_scenes(root), narration, project.load_manifest(root), prof,
                             current_hashes(narration, entries, prof))
    except (StaleManifest, profile_mod.ProfileError, speech.PronunciationError, KeyError) as error:
        print(f"timeline: {error}", file=sys.stderr)
        return 1
    project.write_json(root / "src" / "timeline.json", timeline)
    (root / "out").mkdir(exist_ok=True)
    (root / "out" / "captions.vtt").write_text(captions(timeline, args.caption_offset))
    (root / "out" / "chapters.txt").write_text(chapter_list(timeline, args.caption_offset) + "\n")
    if args.draft:
        print("DRAFT timeline: lengths are estimates and there is no sound; voice the script before rendering")
    print(f"{len(timeline['scenes'])} scenes, {timeline['total'] / 60:.1f} min, {len(timeline['chapters'])} chapters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
