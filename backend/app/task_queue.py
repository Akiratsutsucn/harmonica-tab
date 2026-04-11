"""Lightweight async task queue backed by SQLite."""
import asyncio
import json
import logging
from datetime import datetime, timezone

import aiosqlite

from .database import DB_PATH

logger = logging.getLogger(__name__)


async def enqueue(task_type: str, params: dict) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO tasks (type, status, params) VALUES (?, 'pending', ?)",
            (task_type, json.dumps(params, ensure_ascii=False)),
        )
        task_id = cursor.lastrowid
        await db.commit()
    return task_id


async def get_task(task_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        rows = await db.execute_fetchall("SELECT * FROM tasks WHERE id = ?", (task_id,))
        if not rows:
            return None
        return _row_to_dict(rows[0])


async def list_tasks(status: str | None = None, limit: int = 50) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        if status:
            rows = await db.execute_fetchall(
                "SELECT * FROM tasks WHERE status = ? ORDER BY id DESC LIMIT ?",
                (status, limit),
            )
        else:
            rows = await db.execute_fetchall(
                "SELECT * FROM tasks ORDER BY id DESC LIMIT ?", (limit,)
            )
        return [_row_to_dict(r) for r in rows]


async def update_task(task_id: int, status: str, result: dict | None = None) -> None:
    now = datetime.now(timezone.utc).isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        if result is not None:
            await db.execute(
                "UPDATE tasks SET status = ?, result = ?, updated_at = ? WHERE id = ?",
                (status, json.dumps(result, ensure_ascii=False), now, task_id),
            )
        else:
            await db.execute(
                "UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?",
                (status, now, task_id),
            )
        await db.commit()


async def consume_loop(handlers: dict):
    """Background loop that picks up pending tasks and dispatches to handlers."""
    while True:
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                db.row_factory = aiosqlite.Row
                rows = await db.execute_fetchall(
                    "SELECT * FROM tasks WHERE status = 'pending' ORDER BY id LIMIT 1"
                )
                if not rows:
                    await asyncio.sleep(3)
                    continue
                task = _row_to_dict(rows[0])

            handler = handlers.get(task["type"])
            if not handler:
                await update_task(task["id"], "failed", {"error": f"Unknown task type: {task['type']}"})
                continue

            await update_task(task["id"], "running")
            try:
                result = await handler(task["params"])
                await update_task(task["id"], "done", result or {})
            except Exception as e:
                logger.exception("Task %d failed", task["id"])
                await update_task(task["id"], "failed", {"error": str(e)})

        except asyncio.CancelledError:
            break
        except Exception:
            logger.exception("Task consumer error")
            await asyncio.sleep(5)


def _row_to_dict(row) -> dict:
    d = dict(row)
    for key in ("params", "result"):
        if key in d and isinstance(d[key], str):
            try:
                d[key] = json.loads(d[key])
            except (json.JSONDecodeError, TypeError):
                pass
    return d
