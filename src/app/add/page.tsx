import Link from "next/link";
import SongForm from "@/components/SongForm";

export default function AddSongPage() {
  return (
    <main className="max-w-2xl mx-auto">
      {/* Header */}
      <header className="bg-gradient-to-r from-warm-500 to-warm-400 text-white px-6 py-5 rounded-b-3xl shadow-md flex items-center gap-3">
        <Link
          href="/"
          className="text-white/80 hover:text-white transition-colors text-xl leading-none"
          aria-label="返回"
        >
          ←
        </Link>
        <h1 className="text-xl font-bold tracking-tight">添加歌曲</h1>
      </header>

      <SongForm mode="add" />
    </main>
  );
}
