import { NextRequest } from "next/server";
import fs from "fs";
import path from "path";

const MIME_MAP: Record<string, string> = {
  jpg: "image/jpeg",
  jpeg: "image/jpeg",
  png: "image/png",
  webp: "image/webp",
  mp3: "audio/mpeg",
  wav: "audio/wav",
  m4a: "audio/mp4",
  ogg: "audio/ogg",
};

type Context = { params: Promise<{ path: string[] }> };

export async function GET(_req: NextRequest, { params }: Context) {
  const { path: segments } = await params;

  // Security: reject any segment containing ".."
  if (segments.some((s) => s.includes(".."))) {
    return new Response("Forbidden", { status: 403 });
  }

  const relPath = segments.join("/");
  const absPath = path.join(process.cwd(), "uploads", relPath);

  if (!fs.existsSync(absPath)) {
    return new Response("Not Found", { status: 404 });
  }

  const ext = absPath.split(".").pop()?.toLowerCase() ?? "";
  const contentType = MIME_MAP[ext] ?? "application/octet-stream";

  const buffer = fs.readFileSync(absPath);
  return new Response(buffer, {
    status: 200,
    headers: { "Content-Type": contentType },
  });
}
