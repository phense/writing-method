#!/usr/bin/env bash
# Render on a separate machine reached over SSH, then fetch the result.
# Usage: tools/render-remote.sh [host]     (default: render.host of the profile)
#
# Voicing happens before this step on the authoring machine, so credentials
# never leave it: only the project and its finished sound files are copied.
# The remote machine needs Node, npm and ffmpeg.
set -euo pipefail
cd "$(dirname "$0")/.."
get() { python3 tools/profile.py --get "$1"; }

HOST="${1:-$(get render.host)}"
[[ -n "$HOST" ]] || { echo "no render host: pass one, set render.host in the profile, or use tools/render.sh"; exit 1; }
[[ -f src/timeline.json ]] || { echo "src/timeline.json is missing: run python3 tools/timeline.py"; exit 1; }
if grep -q '"draft": true' src/timeline.json; then
  echo "src/timeline.json is a draft without sound: voice the script, then run python3 tools/timeline.py"; exit 1
fi
ID="$(get video.id)"; LUFS="$(get loudness.lufs)"; PEAK="$(get loudness.true_peak_max)"
REMOTE="$(get render.remote_dir)/$ID"

echo "==> copy project to $HOST:$REMOTE"
ssh "$HOST" "mkdir -p '$REMOTE'"
rsync -a --delete --exclude node_modules --exclude out --exclude stills --exclude takes --exclude env --exclude '*.env' --exclude .git ./ "$HOST:$REMOTE/"

echo "==> render on $HOST"
start=$(date +%s)
# The script arrives on stdin: keep npx and ffmpeg from reading it.
ssh "$HOST" "bash -s" <<REMOTE
set -euo pipefail
export PATH=/opt/homebrew/bin:/usr/local/bin:\$PATH
cd "$REMOTE"
if ! cmp -s package-lock.json node_modules/.package-lock.stamp 2>/dev/null; then
  if [[ -f package-lock.json ]]; then npm ci --no-audit --no-fund; else npm install --no-audit --no-fund; fi
  cp package-lock.json node_modules/.package-lock.stamp
fi
mkdir -p out
nice -n 10 npx remotion render src/index.ts Video out/raw.mp4 --codec=h264 --crf=18 --log=error </dev/null
STATS="\$(ffmpeg -nostdin -v info -i out/raw.mp4 -vn -af "loudnorm=I=$LUFS:TP=$PEAK:LRA=11:print_format=json" -f null - 2>&1 | sed -n '/^{/,/^}/p')"
val() { printf '%s' "\$STATS" | python3 -c "import json,sys; print(json.load(sys.stdin)['\$1'])"; }
ffmpeg -nostdin -v error -y -i out/raw.mp4 -c:v copy \
  -af "loudnorm=I=$LUFS:TP=$PEAK:LRA=11:measured_I=\$(val input_i):measured_TP=\$(val input_tp):measured_LRA=\$(val input_lra):measured_thresh=\$(val input_thresh):offset=\$(val target_offset):linear=true" \
  -ar 48000 -c:a aac -b:a 160k -movflags +faststart "out/$ID.mp4"
rm -f out/raw.mp4
REMOTE
mkdir -p out
scp -q "$HOST:$REMOTE/out/$ID.mp4" "out/$ID.mp4"
echo "==> done in $(( $(date +%s) - start )) s: out/$ID.mp4  (next: python3 tools/measure.py all out/$ID.mp4)"
