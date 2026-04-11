"""Batch importer for JSON/CSV jianpu data."""
import csv
import io
import json
import logging
import re

from .validator import validate_notes

logger = logging.getLogger(__name__)

SIMPLE_NOTE_RE = re.compile(r"([1-7])([#b])?([·]*)([-]*)")

SIMPLE_TO_PITCH = {"1": "C", "2": "D", "3": "E", "4": "F", "5": "G", "6": "A", "7": "B"}


def parse_simple_notation(text: str, octave: int = 4) -> list[dict]:
    """Parse simple notation like '1 2 3 4 | 5 - - -' into note dicts."""
    notes = []
    measures = text.strip().split("|")
    for m_idx, measure_text in enumerate(measures, 1):
        tokens = measure_text.strip().split()
        pos = 1
        for token in tokens:
            if token == "0":
                notes.append({
                    "measure": m_idx, "position": pos,
                    "pitch": "C4", "duration": "quarter",
                    "dot": False, "tie": False,
                })
                pos += 1
                continue
            if token == "-":
                continue  # sustain, handled by duration
            m = SIMPLE_NOTE_RE.match(token)
            if not m:
                pos += 1
                continue
            num, accidental, dots, dashes = m.groups()
            pitch_name = SIMPLE_TO_PITCH.get(num, "C")
            if accidental == "#":
                pitch_name += "#"
            oct = octave + len(dots) if dots else octave
            duration = "quarter"
            if dashes:
                dash_count = len(dashes)
                if dash_count >= 3:
                    duration = "whole"
                elif dash_count >= 1:
                    duration = "half"
            notes.append({
                "measure": m_idx, "position": pos,
                "pitch": f"{pitch_name}{oct}", "duration": duration,
                "dot": False, "tie": False,
            })
            pos += 1
    return notes


async def import_json(content: str) -> dict:
    """Import songs from JSON string. Expected format: list of song objects."""
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        return {"error": f"JSON 解析失败: {e}", "imported": 0}

    if isinstance(data, dict):
        data = [data]

    results = []
    for item in data:
        notes = item.get("notes", [])
        errors = validate_notes(notes, item.get("time_signature", "4/4"))
        results.append({
            "song": {
                "title": item.get("title", "未命名"),
                "artist": item.get("artist", ""),
                "key": item.get("key", "C"),
                "time_signature": item.get("time_signature", "4/4"),
                "bpm": item.get("bpm", 120),
            },
            "notes": notes,
            "validation_errors": errors,
        })

    return {"songs": results, "imported": len(results)}


async def import_csv(content: str) -> dict:
    """Import songs from CSV. Columns: title, artist, key, time_signature, notation."""
    reader = csv.DictReader(io.StringIO(content))
    results = []
    for row in reader:
        notation = row.get("notation", "")
        notes = parse_simple_notation(notation) if notation else []
        ts = row.get("time_signature", "4/4")
        errors = validate_notes(notes, ts) if notes else ["无音符数据"]
        results.append({
            "song": {
                "title": row.get("title", "未命名"),
                "artist": row.get("artist", ""),
                "key": row.get("key", "C"),
                "time_signature": ts,
                "bpm": int(row.get("bpm", 120)),
            },
            "notes": notes,
            "validation_errors": errors,
        })

    return {"songs": results, "imported": len(results)}
