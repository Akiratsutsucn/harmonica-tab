import Database from "better-sqlite3";
import path from "path";

// ── Types ────────────────────────────────────────────────────────────────────

export type DbInstance = Database.Database;

interface SongRow {
  id: number;
  title: string;
  artist: string | null;
  audioType: string | null;
  audioPath: string | null;
  createdAt: string;
  updatedAt: string;
}

interface ImageRow {
  id: number;
  songId: number;
  path: string;
  sortOrder: number;
}

// ── Singleton ────────────────────────────────────────────────────────────────

let _db: Database.Database | null = null;

export function getDb(): Database.Database {
  if (_db) return _db;
  const dbPath = path.join(process.cwd(), "harmonica.db");
  _db = new Database(dbPath);
  _db.pragma("journal_mode = WAL");
  _db.pragma("foreign_keys = ON");
  initDb(_db);
  return _db;
}

// ── Schema ───────────────────────────────────────────────────────────────────

export function initDb(db: Database.Database): void {
  db.exec(`
    CREATE TABLE IF NOT EXISTS songs (
      id        INTEGER PRIMARY KEY AUTOINCREMENT,
      title     TEXT    NOT NULL,
      artist    TEXT,
      audioType TEXT,
      audioPath TEXT,
      createdAt TEXT    NOT NULL DEFAULT (datetime('now')),
      updatedAt TEXT    NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS images (
      id        INTEGER PRIMARY KEY AUTOINCREMENT,
      songId    INTEGER NOT NULL REFERENCES songs(id) ON DELETE CASCADE,
      path      TEXT    NOT NULL,
      sortOrder INTEGER NOT NULL DEFAULT 0
    );
  `);
  // Enable foreign keys for this connection (needed for cascade)
  db.pragma("foreign_keys = ON");
}

// ── Songs ────────────────────────────────────────────────────────────────────

interface CreateSongInput {
  title: string;
  artist?: string | null;
  audioType?: string | null;
  audioPath?: string | null;
}

export function createSong(db: Database.Database, input: CreateSongInput): number {
  const stmt = db.prepare(
    `INSERT INTO songs (title, artist, audioType, audioPath)
     VALUES (@title, @artist, @audioType, @audioPath)`
  );
  const result = stmt.run({
    title: input.title,
    artist: input.artist ?? null,
    audioType: input.audioType ?? null,
    audioPath: input.audioPath ?? null,
  });
  return result.lastInsertRowid as number;
}

export function getSong(db: Database.Database, id: number): SongRow | undefined {
  return db.prepare(`SELECT * FROM songs WHERE id = ?`).get(id) as SongRow | undefined;
}

export function listSongs(db: Database.Database, search?: string): SongRow[] {
  if (search) {
    const like = `%${search}%`;
    return db
      .prepare(
        `SELECT * FROM songs
         WHERE title LIKE ? OR artist LIKE ?
         ORDER BY updatedAt DESC`
      )
      .all(like, like) as SongRow[];
  }
  return db.prepare(`SELECT * FROM songs ORDER BY updatedAt DESC`).all() as SongRow[];
}

interface UpdateSongInput {
  title?: string;
  artist?: string | null;
  audioType?: string | null;
  audioPath?: string | null;
}

export function updateSong(db: Database.Database, id: number, input: UpdateSongInput): void {
  const fields: string[] = [];
  const values: Record<string, unknown> = { id };

  if (input.title !== undefined) { fields.push("title = @title"); values.title = input.title; }
  if (input.artist !== undefined) { fields.push("artist = @artist"); values.artist = input.artist; }
  if (input.audioType !== undefined) { fields.push("audioType = @audioType"); values.audioType = input.audioType; }
  if (input.audioPath !== undefined) { fields.push("audioPath = @audioPath"); values.audioPath = input.audioPath; }

  if (fields.length === 0) return;

  fields.push("updatedAt = datetime('now')");
  db.prepare(`UPDATE songs SET ${fields.join(", ")} WHERE id = @id`).run(values);
}

export function deleteSong(db: Database.Database, id: number): void {
  db.prepare(`DELETE FROM songs WHERE id = ?`).run(id);
}

// ── Images ───────────────────────────────────────────────────────────────────

interface AddImageInput {
  songId: number;
  path: string;
  sortOrder: number;
}

export function addImage(db: Database.Database, input: AddImageInput): number {
  const result = db
    .prepare(`INSERT INTO images (songId, path, sortOrder) VALUES (@songId, @path, @sortOrder)`)
    .run(input);
  return result.lastInsertRowid as number;
}

export function getImagesBySong(db: Database.Database, songId: number): ImageRow[] {
  return db
    .prepare(`SELECT * FROM images WHERE songId = ? ORDER BY sortOrder ASC`)
    .all(songId) as ImageRow[];
}

export function deleteImagesBySong(db: Database.Database, songId: number): void {
  db.prepare(`DELETE FROM images WHERE songId = ?`).run(songId);
}

export function deleteImage(db: Database.Database, imageId: number): string | undefined {
  const row = db.prepare(`SELECT path FROM images WHERE id = ?`).get(imageId) as
    | { path: string }
    | undefined;
  if (!row) return undefined;
  db.prepare(`DELETE FROM images WHERE id = ?`).run(imageId);
  return row.path;
}

export function reorderImages(
  db: Database.Database,
  updates: { id: number; sortOrder: number }[]
): void {
  const stmt = db.prepare(`UPDATE images SET sortOrder = @sortOrder WHERE id = @id`);
  const tx = db.transaction((rows: { id: number; sortOrder: number }[]) => {
    for (const row of rows) stmt.run(row);
  });
  tx(updates);
}
