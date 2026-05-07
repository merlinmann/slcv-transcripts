#!/usr/bin/env bash
# Run transcribe_pipeline.sh for all remaining SLCV episodes.
# Sequential (mlx_whisper is the bottleneck; parallelism would fight for GPU).
set -u
cd "$(dirname "$0")/.."
REPO="$(pwd)"
LOG="${REPO}/transcribe.log"
: > "$LOG"

run() {
  local season="$1" slug="$2" fname="$3"
  local final="${REPO}/transcripts/${season}/${slug}.txt"
  if [ -s "$final" ]; then
    echo "[skip] $slug already done" | tee -a "$LOG"
    return
  fi
  echo "=== $(date +%H:%M:%S) START $slug ===" | tee -a "$LOG"
  bash "${REPO}/scripts/transcribe_pipeline.sh" "$season" "$slug" "$fname" 2>&1 | tee -a "$LOG"
  echo "=== $(date +%H:%M:%S) END   $slug ===" | tee -a "$LOG"
}

# S01 — SDTV .m4v (ac3 stream copy works same way)
run s01 s01e02-television             "Stewart Lee's Comedy Vehicle - s01e02 - Television - SDTV.m4v"
run s01 s01e03-political-correctness  "Stewart Lee's Comedy Vehicle - s01e03 - Political Correctness - SDTV.m4v"
run s01 s01e04-financial-crisis       "Stewart Lee's Comedy Vehicle - s01e04 - Financial Crisis - SDTV.m4v"
run s01 s01e05-religion               "Stewart Lee's Comedy Vehicle - s01e05 - Religion - Unknown.m4v"
run s01 s01e06-comedy                 "Stewart Lee's Comedy Vehicle - s01e06 - Comedy - Unknown.m4v"

# S02 — HDTV 720p .mkv
run s02 s02e01-charity   "Stewart Lee's Comedy Vehicle - s02e01 - Charity - HDTV-720p.mkv"
run s02 s02e02-london    "Stewart Lee's Comedy Vehicle - s02e02 - London - HDTV-720p.mkv"
run s02 s02e03-charity   "Stewart Lee's Comedy Vehicle - s02e03 - Charity - HDTV-720p.mkv"
run s02 s02e04-stand-up  "Stewart Lee's Comedy Vehicle - s02e04 - Stand-Up - HDTV-720p.mkv"
run s02 s02e06-democracy "Stewart Lee's Comedy Vehicle - s02e06 - Democracy - HDTV-720p.mkv"

echo "=== ALL DONE $(date +%H:%M:%S) ===" | tee -a "$LOG"
