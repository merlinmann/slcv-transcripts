#!/usr/bin/env python3
"""
Fix common transcription errors in Stewart Lee Comedy Vehicle transcripts.

This script corrects Whisper's common mishearings of proper nouns, UK-specific
terms, and other words that appear frequently in the Comedy Vehicle series.

Usage:
    python3 fix_transcript.py input.txt -o output.txt    # Fix single file
    python3 fix_transcript.py input.txt -i               # Fix in place
    python3 fix_transcript.py directory/                 # Fix all .txt files
    python3 fix_transcript.py input.txt --dry-run        # Preview changes

Adding new corrections:
    Add entries to the REPLACEMENTS list below in the format:
        ("wrong text", "correct text"),

    Matching is case-insensitive and uses word boundaries to prevent
    partial matches (e.g., won't match "Lee Mac" inside "Lee Mack").

Author: Generated with Claude Code
Date: 2026-01-17
"""

import argparse
import re
from pathlib import Path

# Common transcription errors: (wrong, correct)
REPLACEMENTS = [
    # Words and phrases
    ("cravenid is", "craven idiot"),
    ("craven id is", "craven idiot"),
    ("fapping around", "faffing around"),
    ("fapping about", "faffing about"),
    ("some rare old man", "sombrero, man"),
    ("corderoid", "corduroy"),
    ("Huguenos", "Huguenots"),
    ("Tegas", "Tagus"),
    ("Tegas'", "Tagus"),
    ("hoogligan", "hooligan"),
    ("hooker", "hooligan"),  # context: "football hooker" -> "football hooligan"
    ("Odenist", "Odinist"),
    ("Oak Cake", "Oatcake"),
    ("Oatcake Day", "Oatcake Day"),
    ("mental piece", "mantelpiece"),
    ("Mika Miss", "Michaelmas"),
    ("Michael Miss", "Michaelmas"),
    ("Mikael Miss", "Michaelmas"),
    ("Muslim Mika", "Muslim Michaelmas"),
    ("Pantheos", "Pantheist"),
    ("Pantheist Pancake", "Pantheist Pancake"),
    ("swastikers", "swastikas"),
    ("aquatically", "aquatically"),
    ("equatically", "aquatically"),

    # If You Prefer a Milder Comedian (2010)
    ("Caffeine Arrow", "Caffe Nero"),
    ("blind space", "blank space"),

    # Carpet Remnant World (2012)
    ("carpet-rendered world", "Carpet Remnant World"),

    # S02E04 Stand-Up
    ("Pallava", "Palaver"),
    ("Daleg", "Dalek"),

    # S02E01 Charity
    ("Free credit", "free crisps"),
    ("brick pop", "Britpop"),
    ("crisp spender", "crisps bender"),
    ("Sumatra Narangutans", "Sumatran orangutans"),

    # s03e01 Shilbottle specific
    ("KKnave", "Knave"),  # fix double-K from cascading replacements
    ("Naive magazine", "Knave magazine"),
    ("Nave magazine", "Knave magazine"),
    ("NAVE magazine", "Knave magazine"),
    ("nave centre", "Knave centre"),
    ("nave centis", "Knave centis"),
    ("pack soap", "Paxo"),
    ("packs out", "Paxo"),
    ("packet of packs", "packet of Paxo"),
    ("Schillbottle", "Shilbottle"),
    ("Scheele bottle", "Shilbottle"),
    ("shill bottle", "Shilbottle"),
    ("Schealbottle", "Shilbottle"),
    ("shipball", "Shitbottle"),
    ("ship bottle", "shit bottle"),
    ("Lee Mac", "Lee Mack"),
    ("likely Mac", "Lee Mack"),
    ("Butile de Maired", "Bouteille de Merde"),
    ("Bertile de Maire", "Bouteille de Merde"),
    ("Schizer Flasher", "Scheißflasche"),
    ("Shies a Flasher", "Scheißflasche"),
    ("Faudafon", "Vodafone"),
    ("voter phone", "Vodafone"),
    ("voter phones", "Vodafone's"),
    ("Julian Assara", "Julian Assange"),
    ("telethink", "telly thing"),
    ("non-parishable", "non-perishable"),
    ("non-procible", "non-perishable"),
    ("centres fold", "centrefold"),
    ("center's fold", "centrefold"),
    ("centre's fold", "centrefold"),
    ("primate jogging", "Primark jogging"),
    ("Scottish heron addict", "Scottish heroin addict"),
    ("Villendorf", "Willendorf"),
    ("starsy", "Stasi"),
    ("adversorials", "advertorials"),
    ("Sheterton", "Shitterton"),
    ("Dostin Junction", "Dalston Junction"),
    ("Hybril", "Highbury"),
    ("cocktail at Cafe", "Clock Tower Cafe"),
    ("frogs born", "frogspawn"),

    # s03e03 Satire specific
    ("C. Beebe's", "CBeebies"),
    ("CBB's", "CBeebies"),
    ("C Beebe's", "CBeebies"),
    ("Russell Brandon", "Russell Brand"),
    ("Stuart Lake", "Stewart Lee"),
    ("Banana Rama", "Bananarama"),
    ("banana rama", "Bananarama"),
    ("Merton Parkers", "Merton Parkas"),
    ("Martin Parker's", "Merton Parkas"),
    ("Peter Strinkfellow", "Peter Stringfellow"),
    ("Peter String fellow", "Peter Stringfellow"),
    ("Judith Charmeth", "Judith Chalmers"),
    ("your rhino cake", "urinal cake"),
    ("Irrino cake", "urinal cake"),
    ("rhino cake", "urinal cake"),
    ("Hannah Bonnkarter", "Helena Bonham Carter"),
    ("Helen a Bonham Carter", "Helena Bonham Carter"),
    ("Helen of Opkaster", "Helena Bonham Carter"),
    ("Helen a Opkaster", "Helena Bonham Carter"),
    ("Helen Le Bonham Carter", "Helena Bonham Carter"),
    ("Helen a Bonkarter", "Helena Bonham Carter"),
    ("Eric Cantonagh", "Eric Cantona"),
    ("Eric Cantanard", "Eric Cantona"),
    ("Pierre Ball", "Pierre Boulle"),
    ("Pierre Bull", "Pierre Boulle"),
    ("Ben Fogel", "Ben Fogle"),
    ("Joanna Lomley", "Joanna Lumley"),
    ("Longleaked", "Longleat"),
    ("Michaela Stracken", "Michaela Strachan"),
    ("Mongus", "mongoose"),
    ("Anya's soul", "Anusol"),
    ("anus on", "Anusol"),
    ("anosole", "Anusol"),
    ("anosol", "Anusol"),
    ("anusol", "Anusol"),
    ("Bill Naey", "Bill Nighy"),
    ("Bill Nye", "Bill Nighy"),
    ("oscillot", "ocelot"),
    ("Satara", "satire"),
    ("Marvyn May Club", "Mildmay Club"),
    ("Marvel May Club", "Mildmay Club"),
    ("Wild My Club", "Mildmay Club"),
    ("Keith Laman", "Keith Lemon"),
    ("soda cipher", "soda siphon"),
    ("charmed Hester", "Charlton Heston"),
    ("wood lasso", "woodlouse"),
    ("woodlass", "woodlouse"),
    ("dumb dumb bullet", "dum-dum bullet"),
    ("Dumb dumb bullet", "Dum-dum bullet"),
    ("Billy Breng", "Billy Bragg"),
    ("Robin Inz", "Robin Ince"),

    # s03e04 Context specific
    ("Albert Isler", "Albert Ayler"),
    ("Roy Chelby Brown", "Roy Chubby Brown"),
    ("Reg Hunter", "Reginald D. Hunter"),
    ("Dolston", "Dalston"),
    ("Dawson Junction", "Dalston Junction"),
    ("Hugh Edwards", "Huw Edwards"),

    # s03e05 London specific
    ("N Dubs", "N-Dubz"),
    ("Throne of Flood", "Throne of Blood"),
    ("Bovy Tracy", "Bovey Tracey"),
    ("gas street bass", "Gas Street Basin"),
    ("nape on death", "Napalm Death"),
    ("Nape on Death", "Napalm Death"),
    ("steel pulse", "Steel Pulse"),
    ("atomic kitten", "Atomic Kitten"),
    ("Jason Mamford", "Jason Manford"),
    ("Tilda Swinton", "Tilda Swinton"),

    # s03e06 Marriage specific
    ("Vernon K.", "Vernon Kay"),
    ("Vernon K", "Vernon Kay"),
    ("Andrew Graham Dixon", "Andrew Graham-Dixon"),
    ("Kirtschwitters", "Kurt Schwitters"),
    ("Livier Award", "Olivier Award"),
    ("Sugar Cubes", "Sugarcubes"),
    ("sugar cubes", "Sugarcubes"),
    ("Gary Newman", "Gary Numan"),
    ("Gorky's Zygotic Monkey", "Gorky's Zygotic Mynci"),
    ("Bevis's Frond", "Bevis Frond"),
    ("Elma Gantry's Velvet Opera", "Elmer Gantry's Velvet Opera"),
    ("Mrs. Brown's boys", "Mrs Brown's Boys"),
    ("Mrs Brown's boys", "Mrs Brown's Boys"),
    ("Ratcomad", "Ratko Mladić"),
    ("beseptimized", "vasectomized"),
    ("lasectomized", "vasectomized"),
    ("thinking man's crumpy", "thinking man's crumpet"),

    # s04e01 Wealth specific
    ("VAFTA", "BAFTA"),
    ("Baptist", "BAFTAs"),
    ("Salford Keys", "Salford Quays"),
    ("Sulphur Keys", "Salford Quays"),
    ("the reeking", "the Wrekin"),
    ("T V", "TV"),
    ("taddy", "telly"),
    ("Kevin Bridges", "Kevin Bridges"),

    # Names - Paul Nuttall variations
    ("Paul Nuttles", "Paul Nuttall"),
    ("Paul Nuttle", "Paul Nuttall"),
    ("Paul Nuts", "Paul Nuttall"),
    ("Paul Niles", "Paul Nuttall"),
    ("Paul Nutt-Aulz", "Paul Nuttall"),
    ("Paul Knowles", "Paul Nuttall"),
    ("poor nuttles", "Paul Nuttall"),
    ("Poor nuttles", "Paul Nuttall"),

    # UKIP variations
    ("UKIPs", "UKIP"),
    ("UKIPS", "UKIP"),
    ("the UKIPS", "UKIP"),
    ("the UKIPs", "UKIP"),
    ("Eucyps", "UKIP"),
    ("Eukips", "UKIP"),
    ("Eukip", "UKIP"),
    ("you chips", "UKIP"),
    ("you can And I say", "of UKIP, and I say"),

    # Other proper nouns
    ("Stuart Lee", "Stewart Lee"),
    ("Nigel Frange", "Nigel Farage"),
    ("Jeremy Kahn", "Jeremy Kyle"),
    ("Jeremy Carl", "Jeremy Kyle"),
    ("Mickey Flanagan", "Mickey Flanagan"),  # this one is correct

    # Phrases
    ("rat-a-plenty", "raft"),
    ("rat-of-cuddy", "raft"),
    ("improvise rattle", "improvised raft"),
    ("improvised rat", "improvised raft"),
    ("e-count", "eke out"),
    ("pro-bulk area", "pro-Bulgaria"),

    # Common mishearings
    ("psychical little sack", "cynical little sack"),
    ("circle, little sack", "cynical little sack"),
    ("fin't cut", "finned cunt"),
    ("Finn cunt", "finned cunt"),
    ("finned cunt", "finned cunt"),

    # Misc fixes
    ("bloody beaker folk", "Bloody Beaker folk"),
    ("bloody neolithic", "Bloody Neolithic"),
    ("bloody Huguenots", "Bloody Huguenots"),
    ("bloody Anglo-Saxons", "Bloody Anglo-Saxons"),
    ("bloody Indians", "Bloody Indians"),
    ("bloody Poles", "Bloody Poles"),
    ("bloody polls", "Bloody Poles"),
    ("bloody French", "Bloody French"),
]

# Regex-based replacements for more complex patterns
REGEX_REPLACEMENTS = [
    # Fix "football hooker" -> "football hooligan" (context-aware)
    (r'\bfootball\s+hooker\b', 'football hooligan'),
    (r'\bfootballer\s+hooker\b', 'football hooligan'),

    # Fix variations of "of UKIP"
    (r'\bof\s+the\s+UKIP\b', 'of UKIP'),
    (r'\bof\s+UKIP\s+of\s+UKIP\b', 'of UKIP'),

    # Fix "Paul Nuttall of UKIP" variations
    (r"Paul Nuttall'?s?\s+of\s+UKIP", "Paul Nuttall of UKIP"),

    # Normalize multiple spaces
    (r'  +', ' '),
]


def fix_transcript(text: str) -> str:
    """Apply all fixes to the transcript text."""
    result = text

    # Apply simple replacements with word boundary awareness
    for wrong, correct in REPLACEMENTS:
        # Skip if wrong and correct are the same
        if wrong.lower() == correct.lower():
            continue
        # Use word boundaries to avoid partial matches within already-correct words
        # e.g., don't match "Lee Mac" within "Lee Mack"
        pattern = re.compile(r'\b' + re.escape(wrong) + r'\b', re.IGNORECASE)
        result = pattern.sub(correct, result)

    # Apply regex replacements
    for pattern, replacement in REGEX_REPLACEMENTS:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

    return result


def process_file(input_path: Path, output_path: Path = None, in_place: bool = False):
    """Process a single transcript file."""
    text = input_path.read_text(encoding='utf-8')
    fixed = fix_transcript(text)

    if in_place:
        output_path = input_path
    elif output_path is None:
        output_path = input_path.with_stem(input_path.stem + '_fixed')

    output_path.write_text(fixed, encoding='utf-8')

    # Count changes
    original_words = text.split()
    fixed_words = fixed.split()
    changes = sum(1 for a, b in zip(original_words, fixed_words) if a != b)

    print(f"Processed: {input_path.name}")
    print(f"  Output: {output_path.name}")
    print(f"  Approximate word changes: {changes}")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Fix common transcription errors in Stewart Lee transcripts'
    )
    parser.add_argument(
        'input',
        type=Path,
        nargs='+',
        help='Input transcript file(s) or directory'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output file (only valid with single input file)'
    )
    parser.add_argument(
        '-i', '--in-place',
        action='store_true',
        help='Modify files in place'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without writing files'
    )

    args = parser.parse_args()

    # Collect all input files
    input_files = []
    for path in args.input:
        if path.is_dir():
            input_files.extend(path.glob('*.txt'))
        elif path.exists():
            input_files.append(path)
        else:
            print(f"Warning: {path} not found, skipping")

    if not input_files:
        print("No input files found")
        return

    if args.output and len(input_files) > 1:
        print("Error: --output can only be used with a single input file")
        return

    if args.dry_run:
        for f in input_files:
            text = f.read_text(encoding='utf-8')
            fixed = fix_transcript(text)
            if text != fixed:
                print(f"\n=== Changes for {f.name} ===")
                # Show a few example changes
                for wrong, correct in REPLACEMENTS[:10]:
                    if wrong.lower() in text.lower() and wrong.lower() not in fixed.lower():
                        print(f"  '{wrong}' -> '{correct}'")
    else:
        for f in input_files:
            process_file(f, args.output, args.in_place)


if __name__ == '__main__':
    main()
