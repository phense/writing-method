#!/usr/bin/env bash
# Put an opening sequence in front of a finished video.
# Usage: tools/prepend.sh [--reencode] <video.mp4> [output.mp4] [opening.mp4]
#   default output:  <video>-with-opening.mp4
#   default opening: "opening" of the video profile
#
# If both files have the same stream format they are joined without
# re-encoding (seconds, lossless): a video is never encoded twice on the
# standard path. Otherwise both are brought to the profile's format and
# encoded once; the reason is printed.
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
get() { (cd "$HERE" && python3 tools/profile.py --get "$1"); }
FORCE=0
[[ "${1:-}" == "--reencode" ]] && { FORCE=1; shift; }
IN="${1:?usage: prepend.sh [--reencode] <video.mp4> [output.mp4] [opening.mp4]}"
OUT="${2:-${IN%.*}-with-opening.mp4}"
OPENING="${3:-$(get opening)}"
[[ -n "$OPENING" && -f "$OPENING" ]] || { echo "opening sequence not found: '${OPENING}' (set opening in the profile or pass a file)"; exit 1; }
[[ -f "$IN" ]] || { echo "video not found: $IN"; exit 1; }
case "$(realpath "$OPENING")$(realpath "$IN")" in *"'"*) echo "paths with a single quote are not supported: rename the file"; exit 1;; esac

sig() {
  ffprobe -v error -show_entries \
    stream=codec_type,codec_name,profile,width,height,pix_fmt,r_frame_rate,sample_rate,channels \
    -of compact=nk=1 "$1"
}
if [[ $FORCE == 0 && "$(sig "$OPENING")" == "$(sig "$IN")" ]]; then
  LIST="$(mktemp)"; trap 'rm -f "$LIST"' EXIT
  printf "file '%s'\nfile '%s'\n" "$(realpath "$OPENING")" "$(realpath "$IN")" > "$LIST"
  ffmpeg -nostdin -v error -y -f concat -safe 0 -i "$LIST" -c copy -movflags +faststart "$OUT"
  echo "joined without re-encoding: $OUT"
  echo "opening length: $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OPENING") s (use as --offset and --caption-offset)"
  exit 0
fi
[[ $FORCE == 0 ]] && echo "stream formats differ: both parts are encoded once (slower)"
W="$(get picture.width)"; H="$(get picture.height)"; FPS="$(get picture.fps)"
if ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$IN" | grep -q .; then
  AIN=(-i "$IN"); A1="[1:a]"
else
  # a video without sound gets silence, otherwise the join fails
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
  AIN=(-i "$IN" -f lavfi -t "$dur" -i anullsrc=r=48000:cl=stereo); A1="[2:a]"
fi
V="scale=$W:$H:force_original_aspect_ratio=decrease,pad=$W:$H:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=$FPS,format=yuv420p"
A='aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo'
ffmpeg -nostdin -v error -stats -y -i "$OPENING" "${AIN[@]}" -filter_complex \
  "[0:v]$V[v0];[1:v]$V[v1];[0:a]$A[a0];$A1$A[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]" \
  -map '[v]' -map '[a]' -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 160k -ar 48000 \
  -movflags +faststart "$OUT"
echo "joined with one encode: $OUT"
echo "opening length: $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OPENING") s (use as --offset and --caption-offset)"
