"""Music rule validator for jianpu note sequences."""
import re

# Harmonica playable range (10-hole diatonic)
MIN_MIDI = 48  # C3
MAX_MIDI = 96  # C7

CHROMATIC = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

DURATION_VALUES = {
    "whole": 4.0,
    "half": 2.0,
    "quarter": 1.0,
    "eighth": 0.5,
    "sixteenth": 0.25,
}

PITCH_RE = re.compile(r"^([A-G])(#|b)?(\d)$")


def _parse_pitch(pitch: str) -> tuple[str, str | None, int] | None:
    m = PITCH_RE.match(pitch)
    if not m:
        return None
    return m.group(1), m.group(2), int(m.group(3))


def _pitch_to_midi(pitch: str) -> int | None:
    parsed = _parse_pitch(pitch)
    if not parsed:
        return None
    name, accidental, octave = parsed
    base = name
    if accidental == "#":
        base = name + "#"
    elif accidental == "b":
        idx = CHROMATIC.index(name)
        base = CHROMATIC[(idx - 1) % 12]
    if base not in CHROMATIC:
        return None
    return CHROMATIC.index(base) + (octave + 1) * 12


def validate_notes(notes: list[dict], time_signature: str = "4/4") -> list[str]:
    """Validate a note sequence. Returns list of error strings (empty = valid)."""
    errors = []

    if not notes:
        errors.append("音符序列为空")
        return errors

    # Parse time signature
    try:
        beats_per_measure, beat_unit = time_signature.split("/")
        beats_per_measure = int(beats_per_measure)
        beat_unit = int(beat_unit)
        measure_duration = beats_per_measure * (4.0 / beat_unit)
    except (ValueError, ZeroDivisionError):
        errors.append(f"无效拍号: {time_signature}")
        return errors

    # Group by measure
    measures: dict[int, list[dict]] = {}
    for n in notes:
        m = n.get("measure", 0)
        if m not in measures:
            measures[m] = []
        measures[m].append(n)

    for note in notes:
        pitch = note.get("pitch", "")
        duration = note.get("duration", "quarter")

        # Pitch validation
        midi = _pitch_to_midi(pitch)
        if midi is None:
            errors.append(f"无效音高: {pitch}")
        elif midi < MIN_MIDI or midi > MAX_MIDI:
            errors.append(f"音高超出口琴范围: {pitch} (C3-C7)")

        # Duration validation
        if duration not in DURATION_VALUES:
            errors.append(f"无效时值: {duration}")

    # Measure duration check
    for m_num, m_notes in sorted(measures.items()):
        total = 0.0
        for n in m_notes:
            dur = DURATION_VALUES.get(n.get("duration", "quarter"), 1.0)
            if n.get("dot"):
                dur *= 1.5
            total += dur
        if abs(total - measure_duration) > 0.01:
            errors.append(f"第{m_num}小节时值不匹配: 期望{measure_duration}拍, 实际{total}拍")

    return errors
