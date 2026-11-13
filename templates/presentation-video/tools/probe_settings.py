#!/usr/bin/env python3
"""Find out whether a provider setting has any effect on the profile's voice.

Voices one sample line twice without and twice with the setting. A setting
counts as effective only if the change is larger than the spread between
identical runs. Provider documentation is not evidence: a rate setting was
once used for weeks without effect.

Usage: python3 tools/probe_settings.py rate=+10% [--line intro:0]
Costs four short requests; nothing is cached or written to the project.
"""
import argparse
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audio  # noqa: E402
import profile as profile_mod  # noqa: E402
import project  # noqa: E402
import speech  # noqa: E402
import voice_azure  # noqa: E402


def judge(without: list[float], with_setting: list[float]) -> dict:
    """Effective only beyond the spread of identical runs."""
    spread = max(max(without) - min(without), max(with_setting) - min(with_setting))
    change = sum(with_setting) / len(with_setting) - sum(without) / len(without)
    base = sum(without) / len(without)
    return {"spread": round(spread, 3), "change": round(change, 3),
            "change_percent": round(change / base * 100, 1) if base else 0.0,
            "effective": abs(change) > spread}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("setting", help="name=value, for example rate=+10%%")
    parser.add_argument("--line", default=None, help="scene:index of the sample line (default: longest line)")
    parser.add_argument("--env")
    args = parser.parse_args(argv)
    name, _, value = args.setting.partition("=")
    root = project.ROOT
    try:
        prof = profile_mod.load(root)
        if prof["speech"]["provider"] != "azure":
            print("probe_settings: only the Azure path is probed by this tool; for the connector path "
                  "voice the sample twice by hand and compare", file=sys.stderr)
            return 1
        audio.require("ffprobe")
        synth = voice_azure.azure_synth(voice_azure.load_credentials(voice_azure.find_env(root, args.env, prof)))
        entries = speech.load_pronunciation(*speech.pronunciation_paths(root, prof))
        narration = project.load_narration(root)
        if args.line:
            scene, _, index = args.line.partition(":")
            line = narration[scene][int(index)]
        else:
            line = max((l for ls in narration.values() for l in ls), key=lambda l: len(l["text"]))
        body = speech.spoken_ssml(line, entries)
        base = {k: v for k, v in prof["speech"]["settings"].items() if k != name}
        runs = {"without": [], "with": []}
        with tempfile.TemporaryDirectory() as tmp:
            for label, settings in (("without", base), ("with", {**base, name: value})) * 2:
                document = voice_azure.ssml_document(body, prof["speech"]["voice"], prof["language"], settings)
                path = Path(tmp) / f"{label}-{len(runs[label])}.mp3"
                path.write_bytes(voice_azure.with_retry(lambda: synth(document), prof["speech"]["retry_budget"]))
                runs[label].append(audio.duration(path))
    except (voice_azure.CredentialError, voice_azure.ProviderError, profile_mod.ProfileError, audio.ToolMissing) as error:
        print(f"probe_settings: {error}", file=sys.stderr)
        return 1
    result = judge(runs["without"], runs["with"])
    print(f"without {name}: {runs['without']} s")
    print(f"with {name}={value}: {runs['with']} s")
    print(f"spread between identical runs {result['spread']} s, change {result['change']} s ({result['change_percent']} %)")
    print("EFFECTIVE" if result["effective"] else
          "NOT EFFECTIVE: the voice ignores this setting or the value is too small; do not keep it in the profile")
    return 0 if result["effective"] else 2


if __name__ == "__main__":
    sys.exit(main())
