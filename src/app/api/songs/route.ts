import { NextRequest } from "next/server";
import { getDb, listSongs, createSong, getSong, getImagesBySong } from "@/lib/db";

export async function GET(request: NextRequest) {
  const q = request.nextUrl.searchParams.get("q") ?? undefined;
  const db = getDb();
  const songs = listSongs(db, q);
  const result = songs.map((song) => ({
    ...song,
    images: getImagesBySong(db, song.id),
  }));
  return Response.json(result);
}

export async function POST(request: NextRequest) {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return Response.json({ error: "Invalid JSON" }, { status: 400 });
  }

  if (
    typeof body !== "object" ||
    body === null ||
    typeof (body as Record<string, unknown>).title !== "string" ||
    ((body as Record<string, unknown>).title as string).trim() === ""
  ) {
    return Response.json({ error: "title is required" }, { status: 400 });
  }

  const { title, artist, audioType, audioPath } = body as Record<string, unknown>;

  const db = getDb();
  const id = createSong(db, {
    title: (title as string).trim(),
    artist: typeof artist === "string" ? artist : null,
    audioType: typeof audioType === "string" ? audioType : null,
    audioPath: typeof audioPath === "string" ? audioPath : null,
  });

  const song = getSong(db, id);
  const images = getImagesBySong(db, id);
  return Response.json({ ...song, images }, { status: 201 });
}
