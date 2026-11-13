#!/usr/bin/env python3
"""Voice the narration with Azure AI Speech, one request per line.

Each line is stored under a name derived from its spoken content, voice and
settings. Existing files are reused, so a changed sentence costs one request;
files no longer referenced are removed. Measured length and edge silence go
to src/audio-manifest.json, the only source of timing.

Usage:
  python3 tools/voice_azure.py --check          # credential check, no synthesis
  python3 tools/voice_azure.py                  # voice everything that changed
  python3 tools/voice_azure.py --only intro:0,use:3   # sample lines only

Needs: an env file with AZURE_SPEECH_KEY and AZURE_SPEECH_REGION, found via
--env, AZURE_SPEECH_ENV, the profile's env_file, or env/azure-speech.env in
this folder or a parent. The key is never printed.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audio  # noqa: E402
import profile as profile_mod  # noqa: E402
import project  # noqa: E402
import speech  # noqa: E402

VARIABLES = ("AZURE_SPEECH_KEY", "AZURE_SPEECH_REGION")
OWNED = re.compile(r"^.+-\d{2}-[0-9a-f]{10}\.mp3$")


class CredentialError(RuntimeError):
    pass


class RateLimited(RuntimeError):
    def __init__(self, retry_after: float):
        super().__init__("rate limited")
        self.retry_after = retry_after


class ProviderError(RuntimeError):
    pass


def find_env(root: Path, explicit: str | None, prof: dict | None) -> Path:
    chosen = explicit or os.environ.get("AZURE_SPEECH_ENV") or (prof or {}).get("env_file")
    if chosen:
        return Path(chosen).expanduser()
    for folder in [root, *root.parents]:
        candidate = folder / "env" / "azure-speech.env"
        if candidate.is_file():
            return candidate
    raise CredentialError("no credential file: copy env/azure-speech.env.example to env/azure-speech.env, "
                          "or name the file with --env or AZURE_SPEECH_ENV")


def load_credentials(path: Path) -> dict:
    if not path.is_file():
        raise CredentialError(f"credential file not found: {path}")
    values = {}
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    for name in VARIABLES:
        if not values.get(name):
            raise CredentialError(f"{name} is empty or missing in {path}")
    return {name: values[name] for name in VARIABLES}


def ssml_document(body: str, voice: str, language: str, settings: dict) -> str:
    rate = settings.get("rate")
    if rate and rate not in ("+0%", "0%"):
        body = f'<prosody rate="{rate}">{body}</prosody>'
    return ('<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
            f'xml:lang="{language}"><voice name="{voice}">{body}</voice></speak>')


def _request(url: str, key: str, data: bytes | None, headers: dict) -> bytes:
    request = urllib.request.Request(url, data=data, headers={"Ocp-Apim-Subscription-Key": key, **headers})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read()
    except urllib.error.HTTPError as error:
        if error.code == 429:
            try:
                wait = float(error.headers.get("Retry-After") or 10)
            except ValueError:      # the header may carry a date instead of seconds
                wait = 10.0
            raise RateLimited(wait) from None
        if error.code in (401, 403):
            raise CredentialError("the provider rejected the key (check key and region)") from None
        raise ProviderError(f"provider answered HTTP {error.code}") from None
    except urllib.error.URLError as error:
        raise ProviderError(f"provider not reachable: {error.reason}") from None


def azure_synth(credentials: dict):
    url = f"https://{credentials['AZURE_SPEECH_REGION']}.tts.speech.microsoft.com/cognitiveservices/v1"

    def synth(document: str) -> bytes:
        return _request(url, credentials["AZURE_SPEECH_KEY"], document.encode("utf-8"), {
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-48khz-192kbitrate-mono-mp3",
            "User-Agent": "presentation-video",
        })
    return synth


def with_retry(call, budget: int, sleep=time.sleep, report=print):
    """Wait as instructed on rate limits; give up after `budget` waits."""
    for attempt in range(budget + 1):
        try:
            return call()
        except RateLimited as limited:
            if attempt == budget:
                raise ProviderError(f"still rate limited after {budget} waits") from None
            report(f"  rate limited, waiting {limited.retry_after:.0f} s")
            sleep(limited.retry_after)


def measure_file(path: Path) -> dict:
    lead, trail = audio.edge_silence(path)
    return {"duration": audio.duration(path), "lead_silence": lead, "trail_silence": trail}


def voice(narration: dict, entries: list[dict], prof: dict, audio_dir: Path, synth,
          measure=measure_file, only: set | None = None, sleep=time.sleep, report=print) -> dict:
    """Voice lines, reusing existing files. Returns {manifest, new, characters}.

    A provider failure raises ProviderError; files voiced so far stay on disk
    and are reused by the next run.
    """
    settings, voice_name = prof["speech"]["settings"], prof["speech"]["voice"]
    if only is not None:
        unknown = sorted(f"{s}:{i}" for s, i in only if s not in narration or not 0 <= i < len(narration[s]))
        if unknown:
            raise ProviderError("no such narration line: " + ", ".join(unknown))
    audio_dir.mkdir(parents=True, exist_ok=True)
    manifest, used, new, characters = {}, set(), 0, 0
    for scene, lines in narration.items():
        manifest[scene] = []
        for i, line in enumerate(lines):
            if only is not None and (scene, i) not in only:
                continue
            digest = speech.text_hash(line, entries, prof)
            name = speech.audio_name(scene, i, digest)
            path = audio_dir / name
            if not path.exists():
                document = ssml_document(speech.spoken_ssml(line, entries), voice_name, prof["language"], settings)
                try:
                    data = with_retry(lambda: synth(document), prof["speech"]["retry_budget"], sleep, report)
                except (ProviderError, CredentialError) as error:
                    raise ProviderError(f"{error}; stopped at {scene}:{i} after {new} new line(s), "
                                        f"{characters} characters; completed files are kept") from None
                # write beside the target and rename: an interrupted write must
                # never leave a truncated file that later runs would reuse
                partial = path.with_suffix(".part")
                partial.write_bytes(data)
                partial.replace(path)
                new += 1
                characters += len(speech.base_text(line))
                report(f"  new    {name}")
            used.add(name)
            manifest[scene].append({"file": f"audio/{name}", "hash": digest,
                                    "words": project.words(line["text"]), **measure(path)})
    if only is None:
        for stale in audio_dir.glob("*.mp3"):
            if OWNED.match(stale.name) and stale.name not in used:
                stale.unlink()
                # the read-back transcription of a removed sound describes nothing any more
                stale.with_suffix(".words.json").unlink(missing_ok=True)
    return {"manifest": manifest, "new": new, "characters": characters}


def find_voice(voices: list[dict], wanted: str) -> dict | None:
    """The provider's entry for exactly this voice name; never a voice that
    merely starts with the same name."""
    return next((v for v in voices if v.get("ShortName") == wanted), None)


def check(credentials: dict, prof: dict, report=print) -> None:
    """List the provider's voices: proves key and region without synthesis."""
    url = f"https://{credentials['AZURE_SPEECH_REGION']}.tts.speech.microsoft.com/cognitiveservices/voices/list"
    voices = json.loads(with_retry(lambda: _request(url, credentials["AZURE_SPEECH_KEY"], None, {}), 3))
    report(f"credentials accepted, {len(voices)} voices available")
    wanted = prof["speech"]["voice"]
    match = find_voice(voices, wanted)
    if match is None:
        report(f"note: voice {wanted} is not in the provider's list; confirm it with one sample line")
        return
    languages = [l for l in [match.get("Locale"), *(match.get("SecondaryLocaleList") or [])] if l]
    report(f"voice {match.get('ShortName')}: {', '.join(languages)}")
    claimed = [l for l in prof["speech"]["voice_languages"] if l not in languages]
    if claimed:
        report(f"note: the profile lists {', '.join(claimed)} for this voice, the provider does not; "
               "correct speech.voice_languages")


def parse_only(value: str | None) -> set | None:
    if not value:
        return None
    out = set()
    for item in value.split(","):
        scene, _, index = item.strip().partition(":")
        if not scene or not index.isdigit():
            raise ProviderError(f"--only expects scene:index pairs such as intro:0, got {item!r}")
        out.add((scene, int(index)))
    return out


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--only")
    parser.add_argument("--env")
    args = parser.parse_args(argv)
    root = project.ROOT
    try:
        prof = profile_mod.load(root)
        credentials = load_credentials(find_env(root, args.env, prof))
        if args.check:
            check(credentials, prof)
            return 0
        audio.require("ffmpeg", "ffprobe")
        entries = speech.load_pronunciation(*speech.pronunciation_paths(root, prof))
        only = parse_only(args.only)
        for leftover in (root / "public" / "audio").glob("*.part"):
            leftover.unlink()
        result = voice(project.load_narration(root), entries, prof, root / "public" / "audio",
                       azure_synth(credentials), only=only)
    except (CredentialError, ProviderError, profile_mod.ProfileError, speech.PronunciationError, audio.ToolMissing) as error:
        print(f"voice_azure: {error}", file=sys.stderr)
        return 1
    if only is None:
        project.write_json(root / "src" / "audio-manifest.json", result["manifest"])
    lines = sum(len(v) for v in result["manifest"].values())
    seconds = sum(x["duration"] for v in result["manifest"].values() for x in v)
    print(f"{lines} lines, {seconds:.1f} s of speech, {result['new']} new, {result['characters']} characters voiced")
    return 0


if __name__ == "__main__":
    sys.exit(main())
