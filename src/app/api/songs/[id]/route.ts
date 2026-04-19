import { NextRequest } from "next/server";
import fs from "fs";
import path from "path";
import { getDb, getSong, updateSong, deleteSong, getImagesBySong } from "@/lib/db";

type Context = { params: Promise<{ id: string }> };

export async function GET(_req: NextRequest, { params }: Context) {
  const { id } = await params;
  const numId = Number(id);
  if (!Number.isInteger(numId) || numId <= 0) {
    return Response.json({ error: "Invalid id" }, { status: 400 });
  }

  const db = getDb();
  const song = getSong(db, numId);
  if (!song) {
    return Response.json({ error: "Not found" }, { status: 404 });
  }
  return Response.json({ ...song, images: getImagesBySong(db, numId) });
}

export async function PUT(request: NextRequest, { params }: Context) {
  const { id } = await params;
  const numId = Number(id);
  if (!Number.isInteger(numId) || numId <= 0) {
    return Response.json({ error: "Invalid id" }, { status: 400 });
  }

  const db = getDb();
  if (!getSong(db, numId)) {
    return Response.json({ error: "Not found" }, { status: 404 });
  }

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return Response.json({ error: "Invalid JSON" }, { status: 400 });
  }

  const input = body as Record<string, unknown>;
  updateSong(db, numId, {
    title: typeof input.title === "string" ? input.title : undefined,
    artist: input.artist !== undefined ? (typeof input.artist === "string" ? input.artist : null) : undefined,
    audioType: input.audioType !== undefined ? (typeof input.audioType === "string" ? input.audioType : null) : undefined,
    audioPath: input.audioPath !== undefined ? (typeof input.audioPath === "string" ? input.audioPath : null) : undefined,
  });

  const updated = getSong(db, numId);
  return Response.json({ ...updated, images: getImagesBySong(db, numId) });
}

export async function DELETE(_req: NextRequest, { params }: Context) {
  const { id } = await params;
  const numId = Number(id);
  if (!Number.isInteger(numId) || numId <= 0) {
    return Response.json({ error: "Invalid id" }, { status: 400 });
  }

  const db = getDb();
  if (!getSong(db, numId)) {
    return Response.json({ error: "Not found" }, { status: 404 });
  }

  deleteSong(db, numId);

  fs.rmSync(path.join(process.cwd(), "uploads/images", String(numId)), { recursive: true, force: true });
  fs.rmSync(path.join(process.cwd(), "uploads/audio", String(numId)), { recursive: true, force: true });

  return new Response(null, { status: 204 });
}
