import { notFound } from "next/navigation";
import Link from "next/link";
import { getDb, getSong, getImagesBySong } from "@/lib/db";
import SongForm from "@/components/SongForm";
import type { SongWithImages } from "@/types";

type Props = { params: Promise<{ id: string }> };

export default async function EditSongPage({ params }: Props) {
  const { id } = await params;
  const numId = Number(id);
  if (!Number.isInteger(numId) || numId <= 0) notFound();

  const db = getDb();
  const song = getSong(db, numId);
  if (!song) notFound();

  const images = getImagesBySong(db, numId);

  const initialData: SongWithImages = {
    ...song,
    audioType: song.audioType as "file" | "url" | null,
    images,
  };

  return (
    <div className="min-h-screen bg-warm-50">
      {/* Header */}
      <nav className="fixed top-0 left-0 right-0 h-12 bg-warm-50 flex items-center px-3 gap-2 z-10 shadow-sm">
        <Link
          href={`/song/${numId}`}
          className="w-9 h-9 flex items-center justify-center rounded-lg text-warm-600 hover:bg-warm-100"
          aria-label="返回"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </Link>
        <h1 className="flex-1 text-center font-semibold text-warm-800 text-sm">编辑歌曲</h1>
        {/* spacer to balance the back button */}
        <div className="w-9 h-9" />
      </nav>

      <div className="pt-12">
        <SongForm mode="edit" initialData={initialData} />
      </div>
    </div>
  );
}
