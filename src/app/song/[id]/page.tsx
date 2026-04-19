import { notFound } from "next/navigation";
import Link from "next/link";
import { getDb, getSong, getImagesBySong } from "@/lib/db";
import ImageViewer from "@/components/ImageViewer";
import AudioPlayer from "@/components/AudioPlayer";
import DeleteButton from "./DeleteButton";

type Props = { params: Promise<{ id: string }> };

export default async function SongPage({ params }: Props) {
  const { id } = await params;
  const numId = Number(id);
  if (!Number.isInteger(numId) || numId <= 0) notFound();

  const db = getDb();
  const song = getSong(db, numId);
  if (!song) notFound();

  const images = getImagesBySong(db, numId);

  return (
    <div className="flex flex-col h-screen bg-warm-900">
      {/* Top nav */}
      <nav className="fixed top-0 left-0 right-0 h-12 bg-warm-50 flex items-center px-3 gap-2 z-10 shadow-sm">
        <Link
          href="/"
          className="w-9 h-9 flex items-center justify-center rounded-lg text-warm-600 hover:bg-warm-100"
          aria-label="返回"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </Link>

        <h1 className="flex-1 text-center font-semibold text-warm-800 truncate text-sm px-2">
          {song.title}
        </h1>

        <Link
          href={`/song/${numId}/edit`}
          className="w-9 h-9 flex items-center justify-center rounded-lg text-warm-600 hover:bg-warm-100"
          aria-label="编辑"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
          </svg>
        </Link>

        <DeleteButton songId={numId} />
      </nav>

      {/* Main image area */}
      <main className="flex-1 pt-12 pb-16 overflow-hidden">
        <ImageViewer images={images} />
      </main>

      {/* Audio player */}
      <AudioPlayer
        audioType={song.audioType as "file" | "url" | null}
        audioPath={song.audioPath}
      />
    </div>
  );
}
