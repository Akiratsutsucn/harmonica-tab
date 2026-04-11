"""Song search and detail API routes."""
from fastapi import APIRouter, Depends, Query
import aiosqlite

from .database import get_db
from .schemas import SongOut, SongDetail, NoteOut

router = APIRouter(prefix="/api/songs", tags=["songs"])


@router.get("", response_model=list[SongOut])
async def search_songs(
    q: str = Query("", description="Search by title or artist"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: aiosqlite.Connection = Depends(get_db),
):
    offset = (page - 1) * limit
    if q:
        rows = await db.execute_fetchall(
            "SELECT * FROM songs WHERE status='verified' AND (title LIKE ? OR artist LIKE ?) ORDER BY title LIMIT ? OFFSET ?",
            (f"%{q}%", f"%{q}%", limit, offset),
        )
    else:
        rows = await db.execute_fetchall(
            "SELECT * FROM songs WHERE status='verified' ORDER BY title LIMIT ? OFFSET ?",
            (limit, offset),
        )
    return [dict(r) for r in rows]


@router.get("/hot", response_model=list[SongOut])
async def hot_songs(db: aiosqlite.Connection = Depends(get_db)):
    rows = await db.execute_fetchall(
        "SELECT * FROM songs WHERE status='verified' ORDER BY RANDOM() LIMIT 10"
    )
    if not rows:
        rows = await db.execute_fetchall("SELECT * FROM songs ORDER BY id LIMIT 10")
    return [dict(r) for r in rows]


@router.post("/batch", response_model=list[SongOut])
async def batch_songs(ids: list[int], db: aiosqlite.Connection = Depends(get_db)):
    """Get multiple songs by IDs (for favorites)."""
    if not ids:
        return []
    placeholders = ",".join("?" * len(ids))
    rows = await db.execute_fetchall(
        f"SELECT * FROM songs WHERE id IN ({placeholders}) AND status='verified'", ids
    )
    return [dict(r) for r in rows]


@router.get("/{song_id}", response_model=SongDetail)
async def get_song(song_id: int, db: aiosqlite.Connection = Depends(get_db)):
    row = await db.execute_fetchall("SELECT * FROM songs WHERE id = ?", (song_id,))
    if not row:
        from fastapi import HTTPException
        raise HTTPException(404, "Song not found")
    song = dict(row[0])
    notes = await db.execute_fetchall(
        "SELECT * FROM notes WHERE song_id = ? ORDER BY measure, position",
        (song_id,),
    )
    song["notes"] = [dict(n) for n in notes]
    return song
