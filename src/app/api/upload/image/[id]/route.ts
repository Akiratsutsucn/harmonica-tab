import { NextRequest } from "next/server";
import fs from "fs";
import path from "path";
import { getDb, deleteImage } from "@/lib/db";

type Context = { params: Promise<{ id: string }> };

export async function DELETE(_req: NextRequest, { params }: Context) {
  const { id } = await params;
  const imageId = Number(id);
  if (!Number.isInteger(imageId) || imageId <= 0) {
    return Response.json({ error: "Invalid image id" }, { status: 400 });
  }

  const db = getDb();
  const filePath = deleteImage(db, imageId);

  if (filePath === undefined) {
    return Response.json({ error: "Image not found" }, { status: 404 });
  }

  const absPath = path.join(process.cwd(), filePath);
  try {
    fs.rmSync(absPath);
  } catch {
    // File may already be missing — not a fatal error
  }

  return Response.json({ ok: true });
}
