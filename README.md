# Stewart Lee's Comedy Vehicle Transcript Tools

A Python script for correcting common transcription errors in fan-made transcripts of Stewart Lee's Comedy Vehicle (BBC, 2009-2016).

## The Problem

Speech recognition tools like [MacWhisper](https://goodsnooze.gumroad.com/l/macwhisper) struggle with Stewart Lee's material:

- **Obscure references**: Knave magazine, Albert Ayler, Gorky's Zygotic Mynci
- **UK politicians**: Paul Nuttall, Nigel Farage
- **Foreign phrases**: "Bouteille de Merde", "Scheißflasche"
- **Place names**: Shilbottle, Dalston, Bovey Tracey
- **Deliberate mispronunciations**: Part of the comedy

## The Solution

`fix_transcript.py` automatically corrects 180+ common Whisper mishearings specific to Comedy Vehicle episodes.

## Usage

```bash
# Fix a single transcript
python3 scripts/fix_transcript.py input.txt -o output.txt

# Preview changes without writing
python3 scripts/fix_transcript.py input.txt --dry-run

# Fix in place
python3 scripts/fix_transcript.py input.txt -i

# Fix all .txt files in a directory
python3 scripts/fix_transcript.py raw/
```

## Creating Your Own Transcripts

1. **Extract audio** from your video files:
   ```bash
   ffmpeg -i video.mkv -vn -acodec aac -b:a 192k audio.m4a
   ```

2. **Transcribe** using MacWhisper (Large v3 model recommended)

3. **Correct** using this script:
   ```bash
   python3 scripts/fix_transcript.py raw/s03e01.txt -o transcripts/s03e01.txt
   ```

## Adding New Corrections

Edit `scripts/fix_transcript.py` and add to the `REPLACEMENTS` list:

```python
REPLACEMENTS = [
    ("wrong text", "correct text"),
    # ...
]
```

Matching is case-insensitive and uses word boundaries to prevent partial matches.

## Repository Structure

```
slcv-transcripts/
├── scripts/
│   └── fix_transcript.py   # Error correction script
├── transcripts/            # Your corrected transcripts (not in repo)
├── raw/                    # Your MacWhisper output (not in repo)
└── media/                  # Your video/audio files (not in repo)
```

## Contributing

1. Fork the repository
2. Add new corrections to `fix_transcript.py` with a comment noting the episode context
3. Submit a pull request

## Disclaimer

Stewart Lee's Comedy Vehicle is owned by the BBC. This repository contains only tools for personal transcription work. Support the official release.

## License

MIT
