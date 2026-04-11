"""Admin API routes."""
import json

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
import aiosqlite

from .auth import admin_auth
from .database import get_db
from .schemas import (
    SongCreate, SongUpdate, SongOut, SongDetail, NoteOut, NotesUpdate,
    TaskOut, AIGenerateRequest, CrawlRequest, DashboardOut,
    LoginRequest, LoginResponse,
)
from . import task_queue

router = APIRouter(prefix="/api/admin", tags=["admin"])


# --- Auth ---

@router.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest):
    from .auth import _hash_password, ADMIN_PASSWORD
    if req.password != ADMIN_PASSWORD:
        raise HTTPException(403, "密码错误")
    return {"token": _hash_password(ADMIN_PASSWORD)}


# --- Dashboard ---

@router.get("/dashboard", response_model=DashboardOut, dependencies=[Depends(admin_auth)])
async def dashboard(db: aiosqlite.Connection = Depends(get_db)):
    total = (await db.execute_fetchall("SELECT COUNT(*) as c FROM songs"))[0]["c"]
    verified = (await db.execute_fetchall("SELECT COUNT(*) as c FROM songs WHERE status='verified'"))[0]["c"]
    pending = (await db.execute_fetchall("SELECT COUNT(*) as c FROM songs WHERE status='pending'"))[0]["c"]
    rejected = (await db.execute_fetchall("SELECT COUNT(*) as c FROM songs WHERE status='rejected'"))[0]["c"]
    total_tasks = (await db.execute_fetchall("SELECT COUNT(*) as c FROM tasks"))[0]["c"]
    running_tasks = (await db.execute_fetchall("SELECT COUNT(*) as c FROM tasks WHERE status='running'"))[0]["c"]

    source_rows = await db.execute_fetchall("SELECT source, COUNT(*) as c FROM songs GROUP BY source")
    source_stats = {r["source"]: r["c"] for r in source_rows}

    return {
        "total_songs": total,
        "verified_songs": verified,
        "pending_songs": pending,
        "rejected_songs": rejected,
        "total_tasks": total_tasks,
        "running_tasks": running_tasks,
        "source_stats": source_stats,
    }


# --- Songs CRUD ---

@router.get("/songs", response_model=list[SongOut], dependencies=[Depends(admin_auth)])
async def list_songs(
    status: str = Query(None),
    source: str = Query(None),
    q: str = Query(""),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: aiosqlite.Connection = Depends(get_db),
):
    conditions = []
    params = []
    if status:
        conditions.append("status = ?")
        params.append(status)
    if source:
        conditions.append("source = ?")
        params.append(source)
    if q:
        conditions.append("(title LIKE ? OR artist LIKE ?)")
        params.extend([f"%{q}%", f"%{q}%"])

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    offset = (page - 1) * limit
    params.extend([limit, offset])

    rows = await db.execute_fetchall(
        f"SELECT * FROM songs {where} ORDER BY id DESC LIMIT ? OFFSET ?", params
    )
    return [dict(r) for r in rows]


@router.post("/songs", response_model=SongOut, dependencies=[Depends(admin_auth)])
async def create_song(song: SongCreate, db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute(
        "INSERT INTO songs (title, artist, key, time_signature, bpm, source, status) VALUES (?,?,?,?,?,?,?)",
        (song.title, song.artist, song.key, song.time_signature, song.bpm, song.source, song.status),
    )
    await db.commit()
    rows = await db.execute_fetchall("SELECT * FROM songs WHERE id = ?", (cursor.lastrowid,))
    return dict(rows[0])


@router.put("/songs/{song_id}", response_model=SongOut, dependencies=[Depends(admin_auth)])
async def update_song(song_id: int, update: SongUpdate, db: aiosqlite.Connection = Depends(get_db)):
    existing = await db.execute_fetchall("SELECT * FROM songs WHERE id = ?", (song_id,))
    if not existing:
        raise HTTPException(404, "歌曲不存在")

    fields = []
    values = []
    for field, value in update.model_dump(exclude_none=True).items():
        fields.append(f"{field} = ?")
        values.append(value)

    if fields:
        values.append(song_id)
        await db.execute(f"UPDATE songs SET {', '.join(fields)} WHERE id = ?", values)
        await db.commit()

    rows = await db.execute_fetchall("SELECT * FROM songs WHERE id = ?", (song_id,))
    return dict(rows[0])


@router.delete("/songs/{song_id}", dependencies=[Depends(admin_auth)])
async def delete_song(song_id: int, db: aiosqlite.Connection = Depends(get_db)):
    existing = await db.execute_fetchall("SELECT * FROM songs WHERE id = ?", (song_id,))
    if not existing:
        raise HTTPException(404, "歌曲不存在")
    await db.execute("DELETE FROM notes WHERE song_id = ?", (song_id,))
    await db.execute("DELETE FROM songs WHERE id = ?", (song_id,))
    await db.commit()
    return {"ok": True}


# --- Notes ---

@router.get("/songs/{song_id}/notes", response_model=list[NoteOut], dependencies=[Depends(admin_auth)])
async def get_notes(song_id: int, db: aiosqlite.Connection = Depends(get_db)):
    rows = await db.execute_fetchall(
        "SELECT * FROM notes WHERE song_id = ? ORDER BY measure, position", (song_id,)
    )
    return [dict(r) for r in rows]


@router.put("/songs/{song_id}/notes", dependencies=[Depends(admin_auth)])
async def update_notes(song_id: int, body: NotesUpdate, db: aiosqlite.Connection = Depends(get_db)):
    existing = await db.execute_fetchall("SELECT id FROM songs WHERE id = ?", (song_id,))
    if not existing:
        raise HTTPException(404, "歌曲不存在")

    await db.execute("DELETE FROM notes WHERE song_id = ?", (song_id,))
    for n in body.notes:
        await db.execute(
            "INSERT INTO notes (song_id, measure, position, pitch, duration, dot, tie) VALUES (?,?,?,?,?,?,?)",
            (song_id, n.measure, n.position, n.pitch, n.duration, int(n.dot), int(n.tie)),
        )
    await db.commit()
    return {"ok": True, "count": len(body.notes)}


# --- Verify / Reject ---

@router.post("/songs/{song_id}/verify", dependencies=[Depends(admin_auth)])
async def verify_song(song_id: int, db: aiosqlite.Connection = Depends(get_db)):
    existing = await db.execute_fetchall("SELECT id FROM songs WHERE id = ?", (song_id,))
    if not existing:
        raise HTTPException(404, "歌曲不存在")
    await db.execute("UPDATE songs SET status = 'verified', verified = 1 WHERE id = ?", (song_id,))
    await db.commit()
    return {"ok": True}


@router.post("/songs/{song_id}/reject", dependencies=[Depends(admin_auth)])
async def reject_song(song_id: int, db: aiosqlite.Connection = Depends(get_db)):
    existing = await db.execute_fetchall("SELECT id FROM songs WHERE id = ?", (song_id,))
    if not existing:
        raise HTTPException(404, "歌曲不存在")
    await db.execute("UPDATE songs SET status = 'rejected', verified = 0 WHERE id = ?", (song_id,))
    await db.commit()
    return {"ok": True}


# --- Tasks ---

@router.post("/tasks/ai-generate", dependencies=[Depends(admin_auth)])
async def submit_ai_generate(req: AIGenerateRequest):
    task_id = await task_queue.enqueue("ai_generate", req.model_dump())
    return {"task_id": task_id}


@router.post("/tasks/crawl", dependencies=[Depends(admin_auth)])
async def submit_crawl(req: CrawlRequest):
    task_id = await task_queue.enqueue("crawl", req.model_dump())
    return {"task_id": task_id}


@router.post("/tasks/import", dependencies=[Depends(admin_auth)])
async def submit_import(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8")
    fmt = "csv" if file.filename and file.filename.endswith(".csv") else "json"
    task_id = await task_queue.enqueue("batch_import", {"content": content, "format": fmt})
    return {"task_id": task_id}


@router.get("/tasks", response_model=list[TaskOut], dependencies=[Depends(admin_auth)])
async def list_tasks(status: str = Query(None), limit: int = Query(50)):
    return await task_queue.list_tasks(status=status, limit=limit)


@router.get("/tasks/{task_id}", response_model=TaskOut, dependencies=[Depends(admin_auth)])
async def get_task(task_id: int):
    task = await task_queue.get_task(task_id)
    if not task:
        raise HTTPException(404, "任务不存在")
    return task
