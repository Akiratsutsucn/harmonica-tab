import { NextRequest } from "next/server";
import fs from "fs";
import path from "path";
import crypto from "crypto";
import { getDb, updateSong, getSong } from "@/lib/db";

const ALLOWED_MIME = new Set(["audio/mpeg", "audio/wav", "audio/mp4", "audio/ogg", "audio/x-m4a"]);
const ALLOWED_EXT = new Set(["mp3", "wav", "m4a", "ogg"]);

export async function POST(request: NextRequest) {
  let formData: FormData;
  try {
    formData = await request.formData();
  } catch {
    return Response.json({ error: "Invalid form data" }, { status: 400 });
  }

  const file = formData.get("file") as File | null;
  const songIdRaw = formData.get("songId") as string | null;

  if (!file) return Response.json({ error: "file is required" }, { status: 400 });
  if (!songIdRaw) return Response.json({ error: "songId is required" }, { status: 400 });

  const songId = Number(songIdRaw);
  if (!Number.isInteger(songId) || songId <= 0) {
    return Response.json({ error: "Invalid songId" }, { status: 400 });
  }

  const db = getDb();
  if (!getSong(db, songId)) {
    return Response.json({ error: "Song not found" }, { status: 404 });
  }

  const ext = file.name.split(".").pop()?.toLowerCase() ?? "";
  if (!ALLOWED_EXT.has(ext) || !ALLOWED_MIME.has(file.type)) {
    return Response.json({ error: "Only mp3, wav, m4a, ogg audio files are allowed" }, { status: 400 });
  }

  const filename = `${crypto.randomUUID()}.${ext}`;
  const relPath = `uploads/audio/${songId}/${filename}`;
  const absDir = path.join(process.cwd(), "uploads", "audio", String(songId));

  fs.mkdirSync(absDir, { recursive: true });

  const buffer = Buffer.from(await file.arrayBuffer());
  fs.writeFileSync(path.join(absDir, filename), buffer);

  updateSong(db, songId, { audioType: "file", audioPath: relPath });

  return Response.json({ audioType: "file", audioPath: relPath }, { status: 201 });
}
