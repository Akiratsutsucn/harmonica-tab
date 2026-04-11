"""Batch import songs from JSON file directly into the database."""
import asyncio
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from backend.app.database import DB_PATH
import aiosqlite


async def import_songs(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        songs = json.load(f)

    print(f"Importing {len(songs)} songs...")

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        inserted = 0
        skipped = 0

        for song in songs:
            # Check if song already exists
            existing = await db.execute_fetchall(
                "SELECT id FROM songs WHERE title = ? AND artist = ?",
                (song["title"], song.get("artist", "")),
            )
            if existing:
                print(f"  Skip (exists): {song['title']} - {song.get('artist', '')}")
                skipped += 1
                continue

            cursor = await db.execute(
                "INSERT INTO songs (title, artist, key, time_signature, bpm, source, status, verified) VALUES (?,?,?,?,?,?,?,?)",
                (
                    song["title"],
                    song.get("artist", ""),
                    song.get("key", "C"),
                    song.get("time_signature", "4/4"),
                    song.get("bpm", 120),
                    "ai",
                    "verified",
                    1,
                ),
            )
            song_id = cursor.lastrowid

            notes = song.get("notes", [])
            for n in notes:
                await db.execute(
                    "INSERT INTO notes (song_id, measure, position, pitch, duration, dot, tie) VALUES (?,?,?,?,?,?,?)",
                    (
                        song_id,
                        n["measure"],
                        n["position"],
                        n["pitch"],
                        n.get("duration", "quarter"),
                        int(n.get("dot", False)),
                        int(n.get("tie", False)),
                    ),
                )

            inserted += 1
            print(f"  OK: {song['title']} - {song.get('artist', '')} ({len(notes)} notes)")

        await db.commit()
        print(f"\nDone! Inserted: {inserted}, Skipped: {skipped}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "batch_songs.json"
    asyncio.run(import_songs(path))
