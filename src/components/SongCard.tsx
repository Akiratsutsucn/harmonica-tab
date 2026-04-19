"use client";

import Link from "next/link";
import type { SongWithImages } from "@/types";

interface SongCardProps {
  song: SongWithImages;
}

export default function SongCard({ song }: SongCardProps) {
  const firstImage = song.images[0];

  return (
    <Link href={`/song/${song.id}`}>
      <div className="flex items-center gap-4 bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 p-4 cursor-pointer border border-warm-100">
        {/* Thumbnail */}
        <div className="w-16 h-16 rounded-lg overflow-hidden flex-shrink-0 bg-warm-100 flex items-center justify-center">
          {firstImage ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={`/api/files/${firstImage.path}`}
              alt={song.title}
              className="w-full h-full object-cover"
            />
          ) : (
            <span className="text-2xl">🎼</span>
          )}
        </div>

        {/* Info */}
        <div className="flex-1 min-w-0">
          <p className="font-semibold text-warm-800 truncate">{song.title}</p>
          {song.artist && (
            <p className="text-sm text-warm-400 truncate mt-0.5">{song.artist}</p>
          )}
        </div>
      </div>
    </Link>
  );
}
