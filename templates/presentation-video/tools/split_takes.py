#!/usr/bin/env python3
"""Split per-scene takes into one sound file per narration line.

For providers that speak more naturally from a longer passage: the whole
scene is voiced in one generation (through the provider's connector), then
cut at measured word boundaries.

Input:  takes/<scene>-take<N>.mp3        stored immediately; provider links expire
        takes/<scene>-take<N>.words.json word timings ([{"word","start","end"}])
Output: public/audio/<scene>-<nn>-<hash>.mp3 and src/audio-manifest.json

The take that matches the script best is used. A take below the profile's
match threshold is rejected: it skipped, repeated or changed a sentence.
`prompts` prints the exact passage to voice per scene.

Usage: python3 tools/split_takes.py prompts [scene ...]
       python3 tools/split_takes.py [scene ...]
"""
import difflib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audio  # noqa: E402
import profile as profile_mod  # noqa: E402
import project  # noqa: E402
import speech  # noqa: E402
import voice_azure  # noqa: E402


class TakeRejected(RuntimeError):
    pass


def prompt(lines: list[dict], entries: list[dict], tone: str | None) -> str:
    """Passage for one generation: one line per narration line, at most one
    mild tone tag at the start."""
    body = "\n".join(speech.spoken_plain(l, entries) for l in lines)
    return f"{tone} {body}" if tone else body


def score(spoken: list[str], words: list[dict]) -> float:
    ref = [t for line in spoken for t in speech.tokens(line)]
    hyp = [speech.norm(w["word"]) for w in words if speech.norm(w["word"])]
    return difflib.SequenceMatcher(None, ref, hyp, autojunk=False).ratio()


def cuts(spoken: list[str], words: list[dict], total: float) -> list[tuple[float, float]]:
    """Map line ends onto the recognized words; cut in the pause that follows."""
    ref, owner = [], []
    for i, line in enumerate(spoken):
        for token in speech.tokens(line):
            ref.append(token)
            owner.append(i)
    hyp = [(speech.norm(w["word"]), w) for w in words if speech.norm(w["word"])]
    matcher = difflib.SequenceMatcher(None, ref, [h[0] for h in hyp], autojunk=False)
    matched = {}
    for block in matcher.get_matching_blocks():
        for k in range(block.size):
            matched[block.a + k] = block.b + k
    # every line, the last one included, must be heard: a take that drops a
    # short closing sentence still scores high overall
    for i, line in enumerate(spoken):
        if speech.tokens(line) and not any(o == i and r in matched for r, o in enumerate(owner)):
            raise TakeRejected(f"line {i} was not heard in the take ({line[:40]!r}); request a new take")
    bounds = []
    for i in range(len(spoken) - 1):
        j = max(k for k, o in enumerate(owner) if o == i)
        while j >= 0 and (j not in matched or owner[j] != i):
            j -= 1
        if j < 0:
            raise TakeRejected(f"line {i}: no word recognized")
        h = matched[j]
        following = [r for r, o in enumerate(owner) if o == i + 1 and r in matched]
        h2 = matched[following[0]] if following else min(h + 4, len(hyp) - 1)
        span = range(h, max(h + 1, h2))
        # unmatched words (numbers, addresses) in between belong to line i:
        # cut after the last sentence end in the span, else in its largest pause
        ends = [k for k in span if k + 1 < len(hyp) and hyp[k][1]["word"][-1:] in ".!?:"]
        if ends:
            k = ends[-1]
        else:
            pauses = [(hyp[k + 1][1]["start"] - hyp[k][1]["end"], k) for k in span if k + 1 < len(hyp)]
            if not pauses:
                raise TakeRejected(f"line {i}: no pause found to cut after; request a new take")
            k = max(pauses)[1]
        end = hyp[k][1]["end"]
        nxt = hyp[k + 1][1]["start"] if k + 1 < len(hyp) else total
        bounds.append((end + nxt) / 2)
    edges = [0.0, *bounds, total]
    return list(zip(edges[:-1], edges[1:]))


def choose(spoken: list[str], takes: list[tuple[Path, list[dict]]], threshold: float):
    """Best-matching take, or TakeRejected when none reaches the threshold."""
    best = max(((score(spoken, words), path, words) for path, words in takes), key=lambda t: t[0])
    if best[0] < threshold:
        raise TakeRejected(f"best take {best[1].name} matches the script only {best[0]:.2f} "
                           f"(threshold {threshold}); request a new take")
    return best


def replace_scene_sound(out_dir: Path, scene: str, staging: Path) -> None:
    """Replace every sound file of one scene by the pieces cut into staging."""
    own = speech.scene_file(scene)
    for old in out_dir.glob("*.mp3"):
        if own.fullmatch(old.name):
            old.unlink()
            # A line whose text is unchanged keeps its file name, but the sound is new:
            # an old read-back transcription beside it would be read as the new sound's.
            old.with_suffix(".words.json").unlink(missing_ok=True)
    for piece in sorted(staging.glob("*.mp3")):
        shutil.move(str(piece), out_dir / piece.name)


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    root = project.ROOT
    try:
        prof = profile_mod.load(root)
        entries = speech.load_pronunciation(*speech.pronunciation_paths(root, prof))
        narration = project.load_narration(root)
        if argv[:1] == ["prompts"]:
            for scene in argv[1:] or narration:
                print(f"--- {scene}\n{prompt(narration[scene], entries, prof['speech']['tone'])}\n")
            return 0
        audio.require("ffmpeg", "ffprobe")
        manifest = project.load_manifest(root)
        out_dir = root / "public" / "audio"
        out_dir.mkdir(parents=True, exist_ok=True)
        for scene in argv or narration:
            lines = narration[scene]
            spoken = [speech.spoken_plain(l, entries) for l in lines]
            paths = sorted((root / "takes").glob(f"{scene}-take*.mp3"))
            if not paths:
                print(f"{scene}: no take stored, skipped")
                continue
            takes = []
            for path in paths:
                words = path.with_suffix(".words.json")
                if not words.is_file():
                    raise FileNotFoundError(f"{words.name} is missing; transcribe the take first")
                takes.append((path, project.read_json(words)))
            ratio, take, words = choose(spoken, takes, prof["speech"]["match_threshold"])
            parts = cuts(spoken, words, audio.duration(take))
            # cut into a staging folder; the scene's existing sound is replaced
            # only after every line was cut, so a rejected or failed take
            # never destroys accepted sound
            entries_out = []
            with tempfile.TemporaryDirectory(dir=out_dir) as staging:
                for i, (start, end) in enumerate(parts):
                    digest = speech.text_hash(lines[i], entries, prof)
                    target = Path(staging) / speech.audio_name(scene, i, digest)
                    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
                                    "-i", str(take), "-ar", "48000", "-ac", "1", "-b:a", "192k", str(target)], check=True)
                    entries_out.append({"file": f"audio/{target.name}", "hash": digest,
                                        "words": project.words(lines[i]["text"]), **voice_azure.measure_file(target)})
                replace_scene_sound(out_dir, scene, Path(staging))
            manifest[scene] = entries_out
            print(f"{scene}: {take.name} (match {ratio:.2f}), {len(lines)} lines")
        order = {key: i for i, key in enumerate(narration)}
        manifest = dict(sorted(((k, v) for k, v in manifest.items() if k in order), key=lambda kv: order[kv[0]]))
        project.write_json(root / "src" / "audio-manifest.json", manifest)
    except (TakeRejected, FileNotFoundError, audio.ToolMissing, profile_mod.ProfileError,
            speech.PronunciationError, subprocess.CalledProcessError, KeyError) as error:
        print(f"split_takes: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
