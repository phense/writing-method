"""Read the files of one video project. Shared by all tools."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINE_FIELDS = {"text", "speak", "show", "min", "notice"}
SCENE_FIELDS = {"key", "chapter", "message", "sources", "unverified", "no_claims"}


def read_json(path: Path):
    return json.loads(Path(path).read_text())


def load_narration(root: Path = ROOT) -> dict:
    return read_json(root / "src" / "narration.json")


def load_scenes(root: Path = ROOT) -> list[dict]:
    return read_json(root / "src" / "scenes.json")


def load_manifest(root: Path = ROOT) -> dict:
    path = root / "src" / "audio-manifest.json"
    return read_json(path) if path.is_file() else {}


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def words(text: str) -> int:
    return len(text.replace("`", "").split())
