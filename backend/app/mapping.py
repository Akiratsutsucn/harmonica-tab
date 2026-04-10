"""Paddy Richter & Standard Richter harmonica hole mapping engine."""

# Chromatic scale (sharps notation)
CHROMATIC = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Standard Richter layout for C harmonica: (blow, draw) per hole 1-10
STANDARD_RICHTER_C = [
    ("C4", "D4"),   # 1
    ("E4", "G4"),   # 2
    ("G4", "B4"),   # 3
    ("C5", "D5"),   # 4
    ("E5", "F5"),   # 5
    ("G5", "A5"),   # 6
    ("C6", "B5"),   # 7
    ("E6", "D6"),   # 8
    ("G6", "F6"),   # 9
    ("C7", "A6"),   # 10
]

# Paddy Richter: hole 3 blow changed from G4 to A4
PADDY_RICHTER_C = [
    ("C4", "D4"),   # 1
    ("E4", "G4"),   # 2
    ("A4", "B4"),   # 3  <-- only difference
    ("C5", "D5"),   # 4
    ("E5", "F5"),   # 5
    ("G5", "A5"),   # 6
    ("C6", "B5"),   # 7
    ("E6", "D6"),   # 8
    ("G6", "F6"),   # 9
    ("C7", "A6"),   # 10
]

# Jianpu number mapping: C=1, D=2, E=3, F=4, G=5, A=6, B=7
NOTE_TO_JIANPU = {"C": "1", "D": "2", "E": "3", "F": "4", "G": "5", "A": "6", "B": "7"}

# All supported harmonica keys and their semitone offset from C
KEY_OFFSETS = {
    "C": 0, "Db": 1, "D": 2, "Eb": 3, "E": 4, "F": 5,
    "F#": 6, "G": 7, "Ab": 8, "A": 9, "Bb": 10, "B": 11,
}


def _parse_note(note_str: str) -> tuple[str, int]:
    """Parse 'C#4' -> ('C#', 4)."""
    if note_str[1] == "#":
        return note_str[:2], int(note_str[2:])
    return note_str[0], int(note_str[1:])


def _note_to_midi(note_str: str) -> int:
    name, octave = _parse_note(note_str)
    return CHROMATIC.index(name) + (octave + 1) * 12


def _midi_to_note(midi: int) -> str:
    name = CHROMATIC[midi % 12]
    octave = midi // 12 - 1
    return f"{name}{octave}"


def _transpose_layout(layout: list[tuple[str, str]], semitones: int) -> list[tuple[str, str]]:
    result = []
    for blow, draw in layout:
        b_midi = _note_to_midi(blow) + semitones
        d_midi = _note_to_midi(draw) + semitones
        result.append((_midi_to_note(b_midi), _midi_to_note(d_midi)))
    return result


def _note_to_jianpu(note_str: str, base_octave: int = 4) -> dict:
    """Convert note string to jianpu representation.

    Returns dict with:
      - number: 1-7
      - octave_dots: 0 = middle, positive = dots above, negative = dots below
      - sharp: bool
    """
    name, octave = _parse_note(note_str)
    sharp = "#" in name
    base_name = name.replace("#", "")
    return {
        "number": int(NOTE_TO_JIANPU[base_name]),
        "octave_dots": octave - base_octave,
        "sharp": sharp,
    }


def get_mapping(key: str = "C", tuning: str = "paddy") -> list[dict]:
    """Get full hole mapping for a given key and tuning.

    Returns list of 10 dicts (hole 1-10), each with:
      - hole: int
      - blow: {note, jianpu}
      - draw: {note, jianpu}
    """
    base = PADDY_RICHTER_C if tuning == "paddy" else STANDARD_RICHTER_C
    offset = KEY_OFFSETS.get(key, 0)
    layout = _transpose_layout(base, offset)

    # Determine base octave from hole 1 blow
    _, base_oct = _parse_note(layout[0][0])

    result = []
    for i, (blow, draw) in enumerate(layout):
        result.append({
            "hole": i + 1,
            "blow": {"note": blow, "jianpu": _note_to_jianpu(blow, base_oct)},
            "draw": {"note": draw, "jianpu": _note_to_jianpu(draw, base_oct)},
        })
    return result


def find_hole(pitch: str, key: str = "C", tuning: str = "paddy") -> list[dict]:
    """Find which hole(s) produce a given pitch.

    Args:
        pitch: note like 'C5', 'A4'
        key: harmonica key
        tuning: 'paddy' or 'standard'

    Returns list of matches: [{hole, action: 'blow'|'draw'}]
    """
    target_midi = _note_to_midi(pitch)
    base = PADDY_RICHTER_C if tuning == "paddy" else STANDARD_RICHTER_C
    offset = KEY_OFFSETS.get(key, 0)
    layout = _transpose_layout(base, offset)

    matches = []
    for i, (blow, draw) in enumerate(layout):
        if _note_to_midi(blow) == target_midi:
            matches.append({"hole": i + 1, "action": "blow"})
        if _note_to_midi(draw) == target_midi:
            matches.append({"hole": i + 1, "action": "draw"})
    return matches
