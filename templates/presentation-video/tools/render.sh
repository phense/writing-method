#!/usr/bin/env bash
# Render the video on this machine and normalize its loudness.
# Usage: tools/render.sh            -> out/<video id>.mp4
#
# Voice the script and run tools/timeline.py first. The video is encoded once;
# the loudness pass copies the picture and re-encodes only the sound.
set -euo pipefail
cd "$(dirname "$0")/.."
get() { python3 tools/profile.py --get "$1"; }

[[ -f src/timeline.json ]] || { echo "src/timeline.json is missing: run python3 tools/timeline.py"; exit 1; }
if grep -q '"draft": true' src/timeline.json; then
  echo "src/timeline.json is a draft without sound: voice the script, then run python3 tools/timeline.py"; exit 1
fi
ID="$(get video.id)"; LUFS="$(get loudness.lufs)"; PEAK="$(get loudness.true_peak_max)"
mkdir -p out
npx remotion render src/index.ts Video out/raw.mp4 --codec=h264 --crf=18 --log=error </dev/null
# Remotion's mix is quiet. Two passes: measure, then correct linearly, so the
# result lands on the target instead of near it.
STATS="$(ffmpeg -nostdin -v info -i out/raw.mp4 -vn -af "loudnorm=I=$LUFS:TP=$PEAK:LRA=11:print_format=json" -f null - 2>&1 | sed -n '/^{/,/^}/p')"
val() { printf '%s' "$STATS" | python3 -c "import json,sys; print(json.load(sys.stdin)['$1'])"; }
ffmpeg -nostdin -v error -y -i out/raw.mp4 -c:v copy \
  -af "loudnorm=I=$LUFS:TP=$PEAK:LRA=11:measured_I=$(val input_i):measured_TP=$(val input_tp):measured_LRA=$(val input_lra):measured_thresh=$(val input_thresh):offset=$(val target_offset):linear=true" \
  -ar 48000 -c:a aac -b:a 160k -movflags +faststart "out/$ID.mp4"
rm -f out/raw.mp4
echo "rendered: out/$ID.mp4  (next: python3 tools/measure.py all out/$ID.mp4)"
