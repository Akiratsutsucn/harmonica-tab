"""Database setup and models."""
import aiosqlite
import os

DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "..", "harmonica.db"))


async def get_db():
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                artist TEXT NOT NULL DEFAULT '',
                key TEXT NOT NULL DEFAULT 'C',
                time_signature TEXT NOT NULL DEFAULT '4/4',
                bpm INTEGER DEFAULT 120,
                source TEXT DEFAULT 'manual',
                verified INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                song_id INTEGER NOT NULL,
                measure INTEGER NOT NULL,
                position INTEGER NOT NULL,
                pitch TEXT NOT NULL,
                duration TEXT NOT NULL DEFAULT 'quarter',
                dot INTEGER DEFAULT 0,
                tie INTEGER DEFAULT 0,
                FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_notes_song ON notes(song_id, measure, position);
            CREATE INDEX IF NOT EXISTS idx_songs_title ON songs(title);
        """)
        await db.commit()
