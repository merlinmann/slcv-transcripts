#!/usr/bin/env bash
# Extract audio from Stewart Lee specials on Tiborg -> 16k mono mp3 locally.
set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${REPO}/media/audio/specials"
mkdir -p "${OUT}"
LOG="${REPO}/specials.log"
: > "${LOG}"

extract() {
  local slug="$1"
  local rel="$2"
  local mp3_out="${OUT}/${slug}.mp3"
  if [ -s "${mp3_out}" ]; then echo "[skip] ${slug}" | tee -a "${LOG}"; return; fi

  echo "=== $(date +%H:%M:%S) ${slug} ===" | tee -a "${LOG}"
  local src="/volume1/hello/plex/Movies/${rel}"
  local staging="/tmp/slcv-${slug}.mka"
  local local_mka="${OUT}/${slug}.mka"

  echo "[${slug}] 1/3 extract on tiborg" | tee -a "${LOG}"
  ssh -n tiborg "ffmpeg -y -i \"${src}\" -map 0:a:0 -c:a copy ${staging} 2>/dev/null && ls -la ${staging}" 2>&1 | grep -vE "WARNING|post-quantum|store now|may need|openssh" | tail -1 | tee -a "${LOG}"

  echo "[${slug}] 2/3 pull local" | tee -a "${LOG}"
  ssh -n tiborg "cat ${staging}" 2>/dev/null > "${local_mka}"
  ls -la "${local_mka}" | tee -a "${LOG}"

  echo "[${slug}] 3/3 convert to mp3" | tee -a "${LOG}"
  ffmpeg -y -i "${local_mka}" -c:a libmp3lame -b:a 96k -ar 16000 -ac 1 "${mp3_out}" 2>/dev/null
  rm -f "${local_mka}"
  ls -la "${mp3_out}" | tee -a "${LOG}"
  ssh -n tiborg "rm -f ${staging}" 2>/dev/null
}

extract "stand-up-comedian-2005"     "Stewart Lee - Stand-Up Comedian (2005)/Stewart Lee Stand-Up Comedian (2005) [DVD][]-RZ.m4v"
extract "41st-best-standup-2008"     "Stewart Lee- 41st Best Stand-Up Ever! (2008)/Stewart Lee 41st Best Stand-Up Ever! (2008) [WEBRip-1080p][].mp4"
extract "milder-comedian-2010"       "Stewart Lee - If You Prefer a Milder Comedian, Please Ask for One (2010)/Stewart Lee If You Prefer a Milder Comedian Please Ask for One (2010) [WEBDL-1080p][]-monkee.mkv"
extract "carpet-remnant-world-2012"  "Stewart Lee- Carpet Remnant World (2012)/Stewart Lee Carpet Remnant World (2012) [WEBDL-1080p][]-monkee.mkv"
extract "snowflake-2022"             "Stewart Lee- Snowflake (2022)/Stewart Lee Snowflake (2022) [WEBDL-1080p][]-playWEB.mkv"
extract "tornado-2022"               "Stewart Lee- Tornado (2022)/Stewart Lee Tornado (2022) [WEBRip-1080p][]-LAMA.mp4"
extract "basic-lee-2024"             "Stewart Lee, Basic Lee- Live at The Lowry (2024)/Stewart Lee Basic Lee Live at The Lowry (2024) [WEBRip-1080p][]-LAMA.mp4"

echo "=== ALL DONE $(date +%H:%M:%S) ===" | tee -a "${LOG}"
ls -la "${OUT}"/*.mp3 | tee -a "${LOG}"
