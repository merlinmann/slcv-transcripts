#!/usr/bin/env bash
# Full pipeline: Tiborg mkv/m4v -> AC3 stream copy -> local mp3 -> mlx_whisper -> fix_transcript
# Usage: transcribe_pipeline.sh "<season>" "<episode-slug>" "<tiborg-filename>"
# Example: transcribe_pipeline.sh s02 s02e02-london "Stewart Lee's Comedy Vehicle - s02e02 - London - HDTV-720p.mkv"

set -euo pipefail

SEASON="$1"
SLUG="$2"
TIBORG_FILE="$3"

REPO="/Users/merlin/Documents/Repositories/slcv-transcripts"
TIBORG_DIR="/volume1/hello/plex/TV/Stewart Lee's Comedy Vehicle/Season ${SEASON#s}"
STAGING="/tmp/slcv-${SLUG}.mka"
LOCAL_AUDIO="${REPO}/media/audio/${SLUG}.mka"
LOCAL_MP3="${REPO}/media/audio/${SLUG}.mp3"
RAW_TXT="${REPO}/raw/${SEASON}/${SLUG}.txt"
FINAL_TXT="${REPO}/transcripts/${SEASON}/${SLUG}.txt"

mkdir -p "${REPO}/raw/${SEASON}" "${REPO}/transcripts/${SEASON}" "${REPO}/media/audio"

echo "[${SLUG}] 1/5 extract AC3 on tiborg"
ssh tiborg "ffmpeg -y -i \"${TIBORG_DIR}/${TIBORG_FILE}\" -map 0:a:0 -c:a copy ${STAGING} 2>/dev/null && ls -la ${STAGING}" 2>&1 | grep -vE "WARNING|post-quantum|store now|may need|openssh" | tail -2

echo "[${SLUG}] 2/5 pull to local"
ssh tiborg "cat ${STAGING}" 2>/dev/null > "${LOCAL_AUDIO}"
ls -la "${LOCAL_AUDIO}"

echo "[${SLUG}] 3/5 convert to 16k mono mp3"
ffmpeg -y -i "${LOCAL_AUDIO}" -c:a libmp3lame -b:a 96k -ar 16000 -ac 1 "${LOCAL_MP3}" 2>/dev/null
rm -f "${LOCAL_AUDIO}"

echo "[${SLUG}] 4/5 mlx_whisper large-v3-turbo"
cd "${REPO}"
mlx_whisper "${LOCAL_MP3}" \
  --model mlx-community/whisper-large-v3-turbo \
  --language en \
  --output-format txt \
  --output-dir "raw/${SEASON}/" \
  --output-name "${SLUG}" 2>&1 | tail -2

echo "[${SLUG}] 5/5 fix_transcript"
python3 scripts/fix_transcript.py "${RAW_TXT}" -o "${FINAL_TXT}" 2>&1 | tail -3

echo "[${SLUG}] DONE -> ${FINAL_TXT}"
