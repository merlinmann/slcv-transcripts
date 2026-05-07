#!/usr/bin/env python3
"""Convert SRT subtitle file to plain transcript text.

Strips cue numbers, timecodes, and SDH annotations like (APPLAUSE), (LAUGHTER),
collapses multi-line cues, de-dupes consecutive identical lines.
"""
import re
import sys
from pathlib import Path

SDH_PATTERN = re.compile(r"\([A-Z][A-Z\s,]+\)")
TAG_PATTERN = re.compile(r"<[^>]+>")
TIMECODE = re.compile(r"\d{2}:\d{2}:\d{2}[,.]\d{3}\s*-->")


def srt_to_text(srt_path: Path) -> str:
    text = srt_path.read_text(encoding="utf-8", errors="replace")
    blocks = re.split(r"\n\s*\n", text.strip())
    lines: list[str] = []
    for block in blocks:
        parts = block.strip().splitlines()
        if not parts:
            continue
        # drop cue index
        if parts[0].strip().isdigit():
            parts = parts[1:]
        # drop timecode line
        if parts and TIMECODE.search(parts[0]):
            parts = parts[1:]
        cue = " ".join(p.strip() for p in parts if p.strip())
        cue = TAG_PATTERN.sub("", cue)
        cue = SDH_PATTERN.sub("", cue).strip()
        cue = re.sub(r"\s+", " ", cue)
        if cue and (not lines or lines[-1] != cue):
            lines.append(cue)
    # paragraph breaks on heuristics: end of sentence + next start with capital
    paragraphs: list[str] = []
    buf: list[str] = []
    for line in lines:
        buf.append(line)
        if re.search(r"[.!?][\"')\]]?$", line):
            paragraphs.append(" ".join(buf))
            buf = []
    if buf:
        paragraphs.append(" ".join(buf))
    return "\n\n".join(paragraphs).strip() + "\n"


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: srt_to_text.py input.srt [output.txt]", file=sys.stderr)
        sys.exit(1)
    src = Path(sys.argv[1])
    out_text = srt_to_text(src)
    if len(sys.argv) >= 3:
        Path(sys.argv[2]).write_text(out_text, encoding="utf-8")
    else:
        sys.stdout.write(out_text)


if __name__ == "__main__":
    main()
