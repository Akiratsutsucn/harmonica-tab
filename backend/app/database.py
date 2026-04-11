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
        await db.execute("PRAGMA foreign_keys = ON")
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
                status TEXT DEFAULT 'verified',
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

            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                params TEXT DEFAULT '{}',
                result TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_notes_song ON notes(song_id, measure, position);
            CREATE INDEX IF NOT EXISTS idx_songs_title ON songs(title);
            CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
        """)
        # Migrate existing songs table if status column missing
        try:
            await db.execute("SELECT status FROM songs LIMIT 1")
        except Exception:
            await db.execute("ALTER TABLE status TEXT DEFAULT 'verified'")
        # Migrate: add difficulty column if missing
        try:
            await db.execute("SELECT difficulty FROM songs LIMIT 1")
        except Exception:
            await db.execute("ALTER TABLE songs ADD COLUMN difficulty INTEGER DEFAULT 1")
        await db.commit()
