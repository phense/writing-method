#!/usr/bin/env python3
"""Load and validate the video profile and the per-video file.

The profile (`video-profile.json`) holds a project's house choices and is
found by walking up from the video project, or through VIDEO_PROFILE.
`video.json` in the video project holds the facts of one video and may
override profile values under "overrides".

Usage: python3 tools/profile.py            # validate and print the result
"""
import copy
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Defaults come from measurements of accepted videos (see the method's
# research notes); every one of them can be changed in the profile.
DEFAULTS = {
    "language": None,
    "speech": {
        "provider": None,          # "azure" or "elevenlabs"
        "voice": None,
        "voice_languages": [],     # languages the voice speaks, e.g. ["de-DE", "en-US"]
        "settings": {},            # provider settings; only probed ones count
        "tone": None,              # ElevenLabs: one mild tag per scene, e.g. "[warm]"
        "model": None,
        "mode": "line",            # "line" or "scene" (scene = split takes)
        "retry_budget": 8,
        "match_threshold": 0.9,
    },
    "pace_wpm": None,              # [low, high]; default depends on the language, see PACE
    "pause": {"line": 0.65, "scene_start": 0.5, "scene_end": 1.0, "caption_lead": 0.15},
    "script": {"max_line_words": 28, "max_sentence_words": 22, "max_minutes": 45},
    "picture": {"width": 1920, "height": 1080, "fps": 30, "min_font_px": 28, "margin_px": 60},
    # peak_tolerance absorbs encoder overshoot and measurement rounding
    "loudness": {"lufs": -16.0, "tolerance": 1.0, "true_peak_max": -1.5, "peak_tolerance": 0.1},
    "pause_tolerance": 0.15,
    "opening": None,               # path to an opening sequence, or null
    "render": {"host": None, "remote_dir": "render"},
    "delivery": {"location": None, "keep_intermediate": False},
    "transcribe": None,            # command; {audio} is replaced; writes <audio>.words.json
    "env_file": None,              # credential file; default: env/azure-speech.env upward
}
# Words per minute of pure speech. German: measured on eleven accepted videos
# (116 to 152). English: published narration guidance (about 150 to 175) and
# one measured sample (172). Other languages: set pace_wpm in the profile
# after measuring an accepted video.
PACE = {"de": [120, 155], "en": [140, 180]}
PACE_FALLBACK = [110, 180]
REQUIRED = ["language", "speech.provider", "speech.voice", "speech.voice_languages"]
VIDEO_REQUIRED = ["id", "title", "audience", "address", "goal", "recreated"]
VIDEO_KEYS = set(VIDEO_REQUIRED) | {"overrides", "pronunciation", "stale_when",
                                     "purpose", "edition", "story_id", "based_on"}


class ProfileError(ValueError):
    pass


def _merge(base: dict, extra: dict, path: str = "") -> dict:
    out = copy.deepcopy(base)
    for key, value in extra.items():
        where = f"{path}.{key}" if path else key
        if key not in base:
            raise ProfileError(f"unknown key: {where}")
        # free-form maps (settings) accept any member
        if isinstance(base[key], dict) and base[key] and isinstance(value, dict):
            out[key] = _merge(base[key], value, where)
        else:
            out[key] = value
    return out


def _get(data: dict, dotted: str):
    for part in dotted.split("."):
        data = data.get(part) if isinstance(data, dict) else None
    return data


def find_profile(start: Path) -> Path:
    env = os.environ.get("VIDEO_PROFILE")
    if env:
        return Path(env)
    for folder in [start, *start.parents]:
        candidate = folder / "video-profile.json"
        if candidate.is_file():
            return candidate
    raise ProfileError("video-profile.json not found here or in any parent folder "
                       "(copy video-profile.example.json, or set VIDEO_PROFILE)")


def validate(profile: dict) -> None:
    for key in REQUIRED:
        if not _get(profile, key):
            raise ProfileError(f"missing required key: {key}")
    speech = profile["speech"]
    if speech["provider"] not in ("azure", "elevenlabs"):
        raise ProfileError("speech.provider must be azure or elevenlabs")
    if speech["mode"] not in ("line", "scene"):
        raise ProfileError("speech.mode must be line or scene")
    # FR-033: narration regularly contains English names and terms.
    langs = {str(l).split("-")[0].lower() for l in speech["voice_languages"]}
    target = profile["language"].split("-")[0].lower()
    missing = [l for l in dict.fromkeys([target, "en"]) if l not in langs]
    if missing:
        raise ProfileError("speech.voice must be multilingual: voice_languages lacks "
                           + ", ".join(missing) + " (target language and English are required)")
    low, high = profile["pace_wpm"]
    if not 0 < low < high:
        raise ProfileError("pace_wpm must be [low, high] with 0 < low < high")
    if profile["pause"]["line"] <= 0:
        raise ProfileError("pause.line must be greater than zero")
    # these values are passed to shell commands, also on the render machine
    for dotted in ("loudness.lufs", "loudness.tolerance", "loudness.true_peak_max", "loudness.peak_tolerance",
                   "picture.width", "picture.height", "picture.fps"):
        if isinstance(_get(profile, dotted), bool) or not isinstance(_get(profile, dotted), (int, float)):
            raise ProfileError(f"{dotted} must be a number")
    for dotted, pattern in (("render.host", r"[A-Za-z0-9_.@-]+"), ("render.remote_dir", r"[A-Za-z0-9_./-]+")):
        value = _get(profile, dotted)
        if value is not None and not re.fullmatch(pattern, str(value)):
            raise ProfileError(f"{dotted} may contain only letters, digits and . _ - / @")


def load_video(root: Path = ROOT) -> dict:
    path = root / "video.json"
    if not path.is_file():
        raise ProfileError(f"{path} not found")
    video = json.loads(path.read_text())
    for key in video:
        if key not in VIDEO_KEYS:
            raise ProfileError(f"unknown key in video.json: {key}")
    for key in VIDEO_REQUIRED:
        if video.get(key) in (None, "", []):
            raise ProfileError(f"missing required key in video.json: {key}")
    # the id becomes a file name and part of shell commands
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", str(video["id"])):
        raise ProfileError("video.json: id may contain only lowercase letters, digits and hyphens")
    return video


def load(root: Path = ROOT, profile_path: Path | None = None) -> dict:
    """Profile with defaults and the video's overrides applied, validated."""
    path = profile_path or find_profile(root)
    profile = _merge(DEFAULTS, json.loads(Path(path).read_text()))
    video = root / "video.json"
    if video.is_file():
        profile = _merge(profile, json.loads(video.read_text()).get("overrides", {}))
    if profile.get("language") and not profile["pace_wpm"]:
        profile["pace_wpm"] = list(PACE.get(profile["language"].split("-")[0].lower(), PACE_FALLBACK))
    validate(profile)
    profile["_path"] = str(path)
    return profile


if __name__ == "__main__":
    try:
        result = load()
        video = load_video()
    except (ProfileError, json.JSONDecodeError) as error:
        sys.exit(f"profile: {error}")
    if sys.argv[1:2] == ["--get"]:
        # one value for shell scripts: profile.py --get loudness.lufs
        value = _get({**result, "video": video}, sys.argv[2])
        if sys.argv[2] == "opening" and value and not Path(value).is_absolute():
            value = str(Path(result["_path"]).parent / value)   # relative to the profile
        print("" if value is None else value)
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
