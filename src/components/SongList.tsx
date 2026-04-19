"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import type { SongWithImages } from "@/types";
import SongCard from "./SongCard";

export default function SongList() {
  const [songs, setSongs] = useState<SongWithImages[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);

    debounceRef.current = setTimeout(async () => {
      setLoading(true);
      try {
        const url = search ? `/api/songs?q=${encodeURIComponent(search)}` : "/api/songs";
        const res = await fetch(url);
        if (!res.ok) throw new Error("Failed to fetch songs");
        const data: SongWithImages[] = await res.json();
        setSongs(data);
      } catch {
        setSongs([]);
      } finally {
        setLoading(false);
      }
    }, 300);

    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, [search]);

  return (
    <div className="px-4 py-6">
      {/* Search */}
      <input
        type="text"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="搜索歌曲..."
        className="w-full bg-white border border-warm-200 rounded-xl px-4 py-3 text-warm-800 placeholder-warm-300 outline-none focus:border-warm-400 transition-colors mb-6"
      />

      {/* Song list */}
      {loading ? (
        <p className="text-center text-warm-300 py-12">加载中...</p>
      ) : songs.length === 0 ? (
        <p className="text-center text-warm-300 py-12">
          还没有歌曲，点击右下角添加吧
        </p>
      ) : (
        <div className="flex flex-col gap-3">
          {songs.map((song) => (
            <SongCard key={song.id} song={song} />
          ))}
        </div>
      )}

      {/* Floating add button */}
      <Link href="/add">
        <button
          className="fixed bottom-6 right-6 w-14 h-14 bg-warm-400 hover:bg-warm-500 text-white text-2xl rounded-full shadow-lg flex items-center justify-center transition-colors"
          aria-label="添加歌曲"
        >
          +
        </button>
      </Link>
    </div>
  );
}
