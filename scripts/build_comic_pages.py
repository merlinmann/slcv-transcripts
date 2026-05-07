#!/usr/bin/env python3
"""Build per-comic quote pages from the corpus."""
from pathlib import Path
import re

ROOT = Path("/Users/merlin/Documents/Repositories/slcv-transcripts")
BOOK = ROOT / "reference/books/how-i-escaped-my-certain-fate.txt"
TRANSCRIPTS = ROOT / "transcripts"
OUT = ROOT / "exports"

COMICS = [
    ("ted-chippington", "Ted Chippington", ["Chippington", "Ted Chippington"],
     "Lee's Origin Story",
     "The man who made Stewart Lee a stand-up. Lee saw Ted open for The Fall in Birmingham in October 1984 and everything changed. <em>How I Escaped My Certain Fate</em> is dedicated to him."),
    ("chris-morris", "Chris Morris", ["Chris Morris"],
     "Creative Peer",
     "Morris interviewed Lee on-camera for the full third and fourth series of <em>Stewart Lee's Comedy Vehicle</em>. Their exchanges are the funniest, meanest, and most affectionate interviews Lee has ever done. Lee calls him \"the shadowy satirist\" in the book."),
    ("richard-herring", "Richard Herring", ["Herring"],
     "Writing Partner Since 1986",
     "They met at Oxford, shared a flat in Acton, and wrote the Lee and Herring radio and TV shows together through the nineties. Lee's comedic vocabulary is half Herring's. In <em>Basic Lee</em> (2024), Lee pauses mid-routine to defend the Richard Herring podcast."),
    ("simon-munnery", "Simon Munnery", ["Simon Munnery", "Munnery"],
     "The Comedy Genius",
     "Lee calls Munnery \"legendary,\" \"always apposite,\" \"the comedy genius.\" Together they ran Cluub Zarathustra, a mid-nineties Dadaist cabaret that included Kevin Eldon, Sally Phillips, Julian Barratt and Richard Thomas. Lee cites Munnery as the source of many of his best jokes."),
    ("kevin-eldon", "Kevin Eldon", ["Kevin Eldon"],
     "The Secret Weapon",
     "Lee and Richard Herring always call him \"the Actor Kevin Eldon.\" Eldon has been in the room since Oranje Boom Boom above a Soho pub in 1989 — Cluub Zarathustra, the early tours, and every time Lee needs a second pair of ears on why a bit isn't working."),
]

BOOK_LABEL = "<em>How I Escaped My Certain Fate</em> (Faber, 2010)"

SPECIALS = {
    "stand-up-comedian-2005": "<em>Stand-Up Comedian</em> (2005)",
    "41st-best-standup-2008": "<em>41st Best Stand-Up</em> (2008)",
    "milder-comedian-2010": "<em>If You Prefer a Milder Comedian</em> (2010)",
    "carpet-remnant-world-2012": "<em>Carpet Remnant World</em> (2012)",
    "snowflake-2022": "<em>Snowflake</em> (2022)",
    "tornado-2022": "<em>Tornado</em> (2022)",
    "basic-lee-2024": "<em>Basic Lee</em> (2024)",
}

EPISODE_NAMES = {
    "s01e01-toilet-books": "S1E1 — Toilet Books",
    "s01e02-television": "S1E2 — Television",
    "s01e03-political-correctness": "S1E3 — Political Correctness",
    "s01e04-financial-crisis": "S1E4 — Financial Crisis",
    "s01e05-religion": "S1E5 — Religion",
    "s01e06-comedy": "S1E6 — Comedy",
    "s02e01-charity": "S2E1 — Charity",
    "s02e02-london": "S2E2 — London",
    "s02e03-charity": "S2E3 — Charity",
    "s02e04-stand-up": "S2E4 — Stand-Up",
    "s02e05-identity": "S2E5 — Identity",
    "s02e06-democracy": "S2E6 — Democracy",
    "s03e01-shilbottle": "S3E1 — Shilbottle",
    "s03e02-england": "S3E2 — England",
    "s03e03-satire": "S3E3 — Satire",
    "s03e04-context": "S3E4 — Context",
    "s03e05-london": "S3E5 — London",
    "s03e06-marriage": "S3E6 — Marriage",
    "s04e01-wealth": "S4E1 — Wealth",
    "s04e02-islamophobia": "S4E2 — Islamophobia",
    "s04e03-patriotism": "S4E3 — Patriotism",
    "s04e04-death": "S4E4 — Death",
    "s04e05-migrants": "S4E5 — Migrants",
    "s04e06-childhood": "S4E6 — Childhood",
}


def clean_ws(text):
    return re.sub(r"\s+", " ", text).strip()


def book_context(patterns, window=260):
    text = BOOK.read_text()
    flat = re.sub(r"\s+", " ", text)
    # Find all match positions, dedup by proximity (same region)
    positions = []
    for p in patterns:
        for m in re.finditer(re.escape(p), flat):
            positions.append(m.start())
    positions.sort()
    merged = []
    for pos in positions:
        if merged and pos - merged[-1] < 120:
            continue
        merged.append(pos)
    hits = []
    for pos in merged:
        start = max(0, pos - window)
        end = min(len(flat), pos + window)
        ctx = flat[start:end].strip()
        if start > 0:
            first_space = ctx.find(" ")
            if first_space > 0 and first_space < 40:
                ctx = "…" + ctx[first_space:]
        if end < len(flat):
            last_space = ctx.rfind(" ")
            if last_space > len(ctx) - 40:
                ctx = ctx[:last_space] + "…"
        hits.append(("BOOK", BOOK_LABEL, ctx))
    return hits


def transcript_context(patterns, window=260):
    hits = []
    seen = set()
    for path in sorted(TRANSCRIPTS.rglob("*.txt")):
        if "Content Provider" in path.name:
            continue
        rel = path.relative_to(TRANSCRIPTS)
        stem = path.stem
        parts = path.parts
        if "specials" in parts:
            label = SPECIALS.get(stem, f"<em>{stem}</em>")
            kind = "SPECIAL"
        elif any(s in parts for s in ("s01", "s02", "s03", "s04")):
            label = f"<em>Stewart Lee's Comedy Vehicle</em>, {EPISODE_NAMES.get(stem, stem)}"
            kind = "SLCV"
        else:
            continue
        flat = re.sub(r"\s+", " ", path.read_text())
        positions = []
        for p in patterns:
            for m in re.finditer(r"\b" + re.escape(p) + r"\b", flat):
                positions.append(m.start())
        positions.sort()
        merged = []
        for pos in positions:
            if merged and pos - merged[-1] < 120:
                continue
            merged.append(pos)
        for pos in merged:
            start = max(0, pos - window)
            end = min(len(flat), pos + window)
            ctx = flat[start:end].strip()
            if start > 0:
                first_space = ctx.find(" ")
                if first_space > 0 and first_space < 40:
                    ctx = "…" + ctx[first_space:]
            if end < len(flat):
                last_space = ctx.rfind(" ")
                if last_space > len(ctx) - 40:
                    ctx = ctx[:last_space] + "…"
            hits.append((kind, label, ctx))
    return hits


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{name} — {tag}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
@font-face {{ font-family: "Equity A"; src: local("Equity Text A"), url("https://bucket.contiguous.me/fonts/equity-text-a-regular.woff2") format("woff2"); font-weight: 400; }}
@font-face {{ font-family: "Equity A"; src: local("Equity Text A Italic"), url("https://bucket.contiguous.me/fonts/equity-text-a-italic.woff2") format("woff2"); font-weight: 400; font-style: italic; }}
@font-face {{ font-family: "Equity Caps"; src: local("Equity Caps A"), url("https://bucket.contiguous.me/fonts/equity-caps-a-regular.woff2") format("woff2"); }}
@font-face {{ font-family: "Concourse 4"; src: local("Concourse T4"), url("https://bucket.contiguous.me/fonts/concourse-t4-regular.woff2") format("woff2"); }}
@font-face {{ font-family: "Triplicate"; src: local("Triplicate T4 Code"), url("https://bucket.contiguous.me/fonts/triplicate-t4-code-regular.woff2") format("woff2"); }}

:root {{
  --moss: #2d5a3a;
  --amber: #c8911f;
  --tobacco: #8a5a2b;
  --paper: #f9f5ec;
  --ink: #1a1a1a;
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body {{
  background: var(--paper);
  color: var(--ink);
  font-family: "Equity A", Georgia, serif;
  font-feature-settings: "liga", "kern", "onum";
  line-height: 1.5;
}}

main {{
  max-width: 740px;
  margin: 0 auto;
  padding: 80px 28px 120px;
}}

.eyebrow {{
  font-family: "Concourse 4", system-ui, sans-serif;
  font-size: 13px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--tobacco);
  margin-bottom: 20px;
}}

h1 {{
  font-size: 54px;
  line-height: 1.05;
  letter-spacing: -0.02em;
  color: var(--moss);
  margin-bottom: 12px;
  font-weight: 400;
}}

h1 .tag {{
  display: block;
  font-style: italic;
  font-size: 32px;
  color: var(--tobacco);
  margin-top: 10px;
  letter-spacing: 0;
}}

.rule {{
  height: 4px;
  background: var(--moss);
  width: 88px;
  margin: 36px 0 32px;
}}

.intro {{
  font-size: 20px;
  line-height: 1.55;
  color: var(--ink);
  margin-bottom: 56px;
}}

h2 {{
  font-family: "Concourse 4", system-ui, sans-serif;
  font-size: 14px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--moss);
  margin: 48px 0 20px;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(45,90,58,0.25);
}}

.quote {{
  padding: 20px 0 20px 20px;
  border-left: 3px solid var(--amber);
  margin-bottom: 22px;
}}

.quote .src {{
  font-family: "Concourse 4", system-ui, sans-serif;
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--tobacco);
  margin-bottom: 8px;
}}

.quote .text {{
  font-size: 17px;
  line-height: 1.55;
  color: var(--ink);
}}

.quote .text em {{
  color: var(--tobacco);
}}

.sig {{
  margin-top: 80px;
  padding-top: 28px;
  border-top: 1px solid rgba(138,90,43,0.3);
  font-family: "Concourse 4", system-ui, sans-serif;
  font-size: 13px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--tobacco);
  text-align: right;
}}

a {{ color: var(--moss); }}
</style>
</head>
<body>
<main>
  <div class="eyebrow">Five Comedians Stewart Lee Respects</div>
  <h1>{name}<span class="tag">{tag}</span></h1>
  <div class="rule"></div>
  <p class="intro">{intro}</p>

{sections}

  <p class="sig">— Merlin Mann · 2026 · <a href="comics-lee-respects.html">back to the portfolio</a></p>
</main>
</body>
</html>
"""


def build_page(slug, name, patterns, tag, intro):
    book_hits = book_context(patterns)
    trans_hits = transcript_context(patterns)

    # Group: Book first (roughly chronological by page appearance), then SLCV by season, then specials
    sections_html = []

    if book_hits:
        sections_html.append("<h2>From the book (2010)</h2>")
        for kind, label, ctx in book_hits:
            sections_html.append(
                f'  <div class="quote"><div class="src">{label}</div><div class="text">{ctx}</div></div>'
            )

    # SLCV grouped by season
    slcv_hits = [h for h in trans_hits if h[0] == "SLCV"]
    if slcv_hits:
        sections_html.append("<h2>Stewart Lee's Comedy Vehicle (BBC, 2009–2016)</h2>")
        for kind, label, ctx in slcv_hits:
            sections_html.append(
                f'  <div class="quote"><div class="src">{label}</div><div class="text">{ctx}</div></div>'
            )

    special_hits = [h for h in trans_hits if h[0] == "SPECIAL"]
    if special_hits:
        sections_html.append("<h2>From the stand-up specials</h2>")
        for kind, label, ctx in special_hits:
            sections_html.append(
                f'  <div class="quote"><div class="src">{label}</div><div class="text">{ctx}</div></div>'
            )

    html = TEMPLATE.format(
        name=name,
        tag=tag,
        intro=intro,
        sections="\n".join(sections_html) if sections_html else "<p><em>No mentions found.</em></p>",
    )
    out_path = OUT / f"comic-{slug}.html"
    out_path.write_text(html)
    print(f"Wrote {out_path} — {len(book_hits)} book, {len(slcv_hits)} SLCV, {len(special_hits)} specials")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for slug, name, patterns, tag, intro in COMICS:
        build_page(slug, name, patterns, tag, intro)
