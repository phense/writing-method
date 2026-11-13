"""Measure sound and video files with ffprobe and ffmpeg."""
import json
import re
import shutil
import subprocess
from pathlib import Path

SILENCE_DB = -40.0


class ToolMissing(RuntimeError):
    pass


def require(*programs: str) -> None:
    for program in programs:
        if not shutil.which(program):
            raise ToolMissing(f"{program} is not installed or not on PATH")


def duration(path: Path) -> float:
    require("ffprobe")
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True)
    return round(float(out.stdout.strip()), 3)


def silences(path: Path, min_len: float = 0.05, threshold: float = SILENCE_DB) -> list[tuple[float, float]]:
    """All silent stretches as (start, end) in seconds."""
    require("ffmpeg")
    log = subprocess.run(["ffmpeg", "-nostdin", "-i", str(path), "-vn", "-af",
                          f"silencedetect=noise={threshold}dB:d={min_len}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: (-?[\d.]+)", log)]
    total = None
    out = []
    for i, start in enumerate(starts):
        if i < len(ends):
            end = ends[i]
        else:
            total = total if total is not None else duration(path)
            end = total
        out.append((max(0.0, start), end))
    return out


def edge_silence(path: Path) -> tuple[float, float]:
    """Silence at the start and at the end of a sound file, in seconds."""
    total = duration(path)
    lead = trail = 0.0
    for start, end in silences(path):
        if start <= 0.02:
            lead = end
        if end >= total - 0.06:
            trail = total - start
    return round(min(lead, total), 3), round(min(trail, total), 3)


def loudness(path: Path) -> dict:
    """Integrated loudness (LUFS) and true peak (dBTP) of a file's sound."""
    require("ffmpeg")
    log = subprocess.run(["ffmpeg", "-nostdin", "-i", str(path), "-vn", "-af",
                          "loudnorm=print_format=json", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    block = json.loads(log[log.rindex("{"):log.rindex("}") + 1])
    return {"lufs": float(block["input_i"]), "true_peak": float(block["input_tp"])}


def video_properties(path: Path) -> dict:
    require("ffprobe")
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "stream=codec_type,width,height,r_frame_rate:format=duration", "-of", "json", str(path)],
                         capture_output=True, text=True, check=True)
    data = json.loads(out.stdout)
    video = next((s for s in data["streams"] if s.get("codec_type") == "video"), {})
    num, den = (video.get("r_frame_rate") or "0/1").split("/")
    return {"width": video.get("width"), "height": video.get("height"),
            "fps": round(int(num) / int(den), 3) if int(den) else 0,
            "duration": round(float(data["format"]["duration"]), 3),
            "has_audio": any(s.get("codec_type") == "audio" for s in data["streams"])}
