"""FastAPI application entry point."""
import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .database import init_db
from .routes_songs import router as songs_router
from .routes_mapping import router as mapping_router
from .routes_admin import router as admin_router
from . import task_queue
from .pipeline.ai_generator import generate_jianpu
from .pipeline.scraper import scrape_jianpu
from .pipeline.importer import import_json, import_csv

logger = logging.getLogger(__name__)

async def _handle_batch_import(params: dict) -> dict:
    content = params.get("content", "")
    fmt = params.get("format", "json")
    if fmt == "csv":
        result = await import_csv(content)
    else:
        result = await import_json(content)

    # Auto-insert valid songs into DB
    if "songs" in result:
        from .database import DB_PATH
        import aiosqlite

        inserted = 0
        async with aiosqlite.connect(DB_PATH) as db:
            for item in result["songs"]:
                if item.get("validation_errors"):
                    continue
                song = item["song"]
                cursor = await db.execute(
                    "INSERT INTO songs (title, artist, key, time_signature, bpm, source, status) VALUES (?,?,?,?,?,?,?)",
                    (song["title"], song["artist"], song["key"], song["time_signature"], song["bpm"], "import", "pending"),
                )
                song_id = cursor.lastrowid
                for n in item["notes"]:
                    await db.execute(
                        "INSERT INTO notes (song_id, measure, position, pitch, duration, dot, tie) VALUES (?,?,?,?,?,?,?)",
                        (song_id, n["measure"], n["position"], n["pitch"], n["duration"],
                         int(n.get("dot", False)), int(n.get("tie", False))),
                    )
                inserted += 1
            await db.commit()
        result["inserted"] = inserted

    return result


TASK_HANDLERS = {
    "ai_generate": generate_jianpu,
    "crawl": scrape_jianpu,
    "batch_import": _handle_batch_import,
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await seed_if_empty()
    consumer = asyncio.create_task(task_queue.consume_loop(TASK_HANDLERS))
    yield
    consumer.cancel()
    try:
        await consumer
    except asyncio.CancelledError:
        pass


app = FastAPI(title="Harmonica Tab API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(songs_router)
app.include_router(mapping_router)
app.include_router(admin_router)

# Serve frontend static files if dist exists
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")
if os.path.isdir(frontend_dist):
    # Static assets (js, css, images)
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    # SPA fallback: serve index.html for non-API routes
    @app.get("/{full_path:path}")
    async def spa_fallback(request: Request, full_path: str):
        # Try to serve static file first
        file_path = os.path.join(frontend_dist, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))


async def seed_if_empty():
    """Seed demo songs on first run."""
    from .database import DB_PATH
    import aiosqlite

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        row = await db.execute_fetchall("SELECT COUNT(*) as c FROM songs")
        if row[0]["c"] > 0:
            return
        await _seed_songs(db)
        await db.commit()


async def _seed_songs(db):
    """Insert demo songs with jianpu note data."""
    songs = _get_seed_data()
    for song in songs:
        cursor = await db.execute(
            "INSERT INTO songs (title, artist, key, time_signature, bpm, source, verified, status) VALUES (?,?,?,?,?,?,?,?)",
            (song["title"], song["artist"], song["key"], song["ts"], song["bpm"], "manual", 1, "verified"),
        )
        song_id = cursor.lastrowid
        for note in song["notes"]:
            await db.execute(
                "INSERT INTO notes (song_id, measure, position, pitch, duration, dot, tie) VALUES (?,?,?,?,?,?,?)",
                (song_id, note[0], note[1], note[2], note[3], note[4] if len(note) > 4 else 0, note[5] if len(note) > 5 else 0),
            )


def _get_seed_data():
    """Return seed song data. Each note: (measure, position, pitch, duration, dot?, tie?)"""
    return [
        {
            "title": "小星星", "artist": "儿歌", "key": "C", "ts": "4/4", "bpm": 100,
            "notes": [
                (1,1,"C4","quarter"), (1,2,"C4","quarter"), (1,3,"G4","quarter"), (1,4,"G4","quarter"),
                (2,1,"A4","quarter"), (2,2,"A4","quarter"), (2,3,"G4","half"),
                (3,1,"F4","quarter"), (3,2,"F4","quarter"), (3,3,"E4","quarter"), (3,4,"E4","quarter"),
                (4,1,"D4","quarter"), (4,2,"D4","quarter"), (4,3,"C4","half"),
                (5,1,"G4","quarter"), (5,2,"G4","quarter"), (5,3,"F4","quarter"), (5,4,"F4","quarter"),
                (6,1,"E4","quarter"), (6,2,"E4","quarter"), (6,3,"D4","half"),
                (7,1,"G4","quarter"), (7,2,"G4","quarter"), (7,3,"F4","quarter"), (7,4,"F4","quarter"),
                (8,1,"E4","quarter"), (8,2,"E4","quarter"), (8,3,"D4","half"),
            ],
        },
        {
            "title": "欢乐颂", "artist": "贝多芬", "key": "C", "ts": "4/4", "bpm": 120,
            "notes": [
                (1,1,"E4","quarter"), (1,2,"E4","quarter"), (1,3,"F4","quarter"), (1,4,"G4","quarter"),
                (2,1,"G4","quarter"), (2,2,"F4","quarter"), (2,3,"E4","quarter"), (2,4,"D4","quarter"),
                (3,1,"C4","quarter"), (3,2,"C4","quarter"), (3,3,"D4","quarter"), (3,4,"E4","quarter"),
                (4,1,"E4","quarter",1), (4,2,"D4","eighth"), (4,3,"D4","half"),
                (5,1,"E4","quarter"), (5,2,"E4","quarter"), (5,3,"F4","quarter"), (5,4,"G4","quarter"),
                (6,1,"G4","quarter"), (6,2,"F4","quarter"), (6,3,"E4","quarter"), (6,4,"D4","quarter"),
                (7,1,"C4","quarter"), (7,2,"C4","quarter"), (7,3,"D4","quarter"), (7,4,"E4","quarter"),
                (8,1,"D4","quarter",1), (8,2,"C4","eighth"), (8,3,"C4","half"),
            ],
        },
        {
            "title": "送别", "artist": "李叔同", "key": "C", "ts": "4/4", "bpm": 80,
            "notes": [
                (1,1,"E4","quarter"), (1,2,"G4","quarter",1), (1,3,"E4","eighth"), (1,4,"G4","quarter"),
                (2,1,"A4","half"), (2,2,"G4","half"),
                (3,1,"E4","quarter"), (3,2,"D4","quarter"), (3,3,"E4","quarter"), (3,4,"G4","quarter"),
                (4,1,"D4","whole"),
                (5,1,"E4","quarter"), (5,2,"G4","quarter",1), (5,3,"E4","eighth"), (5,4,"G4","quarter"),
                (6,1,"A4","half"), (6,2,"G4","half"),
                (7,1,"E4","quarter"), (7,2,"D4","quarter"), (7,3,"E4","quarter"), (7,4,"D4","quarter"),
                (8,1,"C4","whole"),
            ],
        },
        {
            "title": "茉莉花", "artist": "民歌", "key": "C", "ts": "4/4", "bpm": 76,
            "notes": [
                (1,1,"E4","quarter"), (1,2,"E4","quarter"), (1,3,"F4","quarter"), (1,4,"G4","quarter"),
                (2,1,"A4","quarter"), (2,2,"A4","quarter"), (2,3,"G4","half"),
                (3,1,"G4","quarter"), (3,2,"A4","quarter"), (3,3,"G4","quarter"), (3,4,"E4","quarter"),
                (4,1,"D4","half"), (4,2,"E4","half"),
                (5,1,"C4","quarter"), (5,2,"D4","quarter"), (5,3,"E4","quarter"), (5,4,"E4","quarter"),
                (6,1,"D4","quarter"), (6,2,"C4","quarter"), (6,3,"D4","half"),
                (7,1,"E4","quarter"), (7,2,"G4","quarter"), (7,3,"A4","quarter"), (7,4,"G4","quarter"),
                (8,1,"E4","half"), (8,2,"D4","half"),
            ],
        },
        {
            "title": "两只老虎", "artist": "儿歌", "key": "C", "ts": "4/4", "bpm": 120,
            "notes": [
                (1,1,"C4","quarter"), (1,2,"D4","quarter"), (1,3,"E4","quarter"), (1,4,"C4","quarter"),
                (2,1,"C4","quarter"), (2,2,"D4","quarter"), (2,3,"E4","quarter"), (2,4,"C4","quarter"),
                (3,1,"E4","quarter"), (3,2,"F4","quarter"), (3,3,"G4","half"),
                (4,1,"E4","quarter"), (4,2,"F4","quarter"), (4,3,"G4","half"),
                (5,1,"G4","eighth"), (5,2,"A4","eighth"), (5,3,"G4","eighth"), (5,4,"F4","eighth"),
                (5,5,"E4","quarter"), (5,6,"C4","quarter"),
                (6,1,"G4","eighth"), (6,2,"A4","eighth"), (6,3,"G4","eighth"), (6,4,"F4","eighth"),
                (6,5,"E4","quarter"), (6,6,"C4","quarter"),
                (7,1,"C4","quarter"), (7,2,"G3","quarter"), (7,3,"C4","half"),
                (8,1,"C4","quarter"), (8,2,"G3","quarter"), (8,3,"C4","half"),
            ],
        },
        {
            "title": "世上只有妈妈好", "artist": "儿歌", "key": "C", "ts": "4/4", "bpm": 88,
            "notes": [
                (1,1,"G4","quarter"), (1,2,"E4","quarter"), (1,3,"G4","quarter"), (1,4,"A4","quarter"),
                (2,1,"G4","quarter"), (2,2,"E4","quarter"), (2,3,"G4","half"),
                (3,1,"A4","quarter"), (3,2,"G4","quarter"), (3,3,"E4","quarter"), (3,4,"G4","quarter"),
                (4,1,"D4","half"), (4,2,"E4","quarter"), (4,3,"D4","quarter"),
                (5,1,"C4","quarter"), (5,2,"D4","quarter"), (5,3,"E4","quarter"), (5,4,"G4","quarter"),
                (6,1,"A4","half"), (6,2,"G4","half"),
            ],
        },
        {
            "title": "月亮代表我的心", "artist": "邓丽君", "key": "C", "ts": "4/4", "bpm": 72,
            "notes": [
                (1,1,"E4","quarter"), (1,2,"E4","eighth"), (1,3,"F4","eighth"), (1,4,"G4","half"),
                (2,1,"G4","quarter"), (2,2,"A4","quarter"), (2,3,"G4","quarter"), (2,4,"E4","quarter"),
                (3,1,"C4","quarter"), (3,2,"D4","quarter"), (3,3,"E4","half"),
                (4,1,"D4","whole"),
                (5,1,"E4","quarter"), (5,2,"E4","eighth"), (5,3,"F4","eighth"), (5,4,"G4","half"),
                (6,1,"C5","quarter"), (6,2,"B4","quarter"), (6,3,"A4","quarter"), (6,4,"G4","quarter"),
                (7,1,"F4","quarter"), (7,2,"G4","quarter"), (7,3,"A4","half"),
                (8,1,"G4","whole"),
            ],
        },
    ]
