import SongList from "@/components/SongList";

export default function Home() {
  return (
    <main className="max-w-2xl mx-auto">
      {/* Header */}
      <header className="bg-gradient-to-r from-warm-500 to-warm-400 text-white px-6 py-8 rounded-b-3xl shadow-md">
        <h1 className="text-3xl font-bold tracking-tight">🎵 口琴练习</h1>
        <p className="mt-1 text-warm-100 text-sm opacity-90">我的曲库</p>
      </header>

      {/* Song list with search */}
      <SongList />
    </main>
  );
}
