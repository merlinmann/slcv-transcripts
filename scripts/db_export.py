#!/usr/bin/env python3
"""Export speaker-labeled transcripts from the MacWhisper SQLite database.

Matches the S03/S04 raw convention:

    Speaker Name
    Line of dialogue. More dialogue.

    Next Speaker Name
    Next line...

Usage: db_export.py <output_dir>
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path
from typing import Optional

DB_PATH = Path.home() / "Library/Application Support/MacWhisper/Database/main.sqlite"

SLUGS = {
    "s01e02-television": "s01",
    "s01e03-political-correctness": "s01",
    "s01e04-financial-crisis": "s01",
    "s01e05-religion": "s01",
    "s01e06-comedy": "s01",
    "s02e01-charity": "s02",
    "s02e02-london": "s02",
    "s02e03-charity": "s02",
    "s02e04-stand-up": "s02",
    "s02e05-identity": "s02",
    "s02e06-democracy": "s02",
    "stand-up-comedian-2005": "specials",
    "41st-best-standup-2008": "specials",
    "milder-comedian-2010": "specials",
    "carpet-remnant-world-2012": "specials",
    "snowflake-2022": "specials",
    "tornado-2022": "specials",
    "basic-lee-2024": "specials",
}


def export_session(conn: sqlite3.Connection, filename: str, out_path: Path) -> None:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT sp.name, tl.text, tl.start
          FROM transcriptline tl
          JOIN session s ON s.id = tl.sessionId
          JOIN speaker sp ON sp.id = tl.speakerID
         WHERE s.originalFilename = ?
         ORDER BY tl.start
        """,
        (filename,),
    )
    rows = cur.fetchall()

    out: list[str] = []
    current_speaker: Optional[str] = None
    buffer: list[str] = []

    def flush() -> None:
        if current_speaker is None or not buffer:
            return
        out.append(current_speaker)
        out.append(" ".join(t.strip() for t in buffer if t.strip()))
        out.append("")

    for name, text, _start in rows:
        if name != current_speaker:
            flush()
            current_speaker = name
            buffer = [text]
        else:
            buffer.append(text)
    flush()

    out_path.write_text("\n".join(out).strip() + "\n", encoding="utf-8")


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: db_export.py <output_dir>", file=sys.stderr)
        sys.exit(1)
    out_base = Path(sys.argv[1])
    conn = sqlite3.connect(DB_PATH)

    count = 0
    for slug, season in SLUGS.items():
        out_dir = out_base / season
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{slug}.txt"
        export_session(conn, slug, out_path)
        count += 1
        print(f"wrote {out_path}")
    print(f"done: {count} files")


if __name__ == "__main__":
    main()
