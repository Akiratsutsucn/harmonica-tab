"use client";

import { useRef, useState } from "react";
import type { SongImage } from "@/types";

interface ImageUploaderProps {
  songId: number | null;
  images: SongImage[];
  onImagesChange: (images: SongImage[]) => void;
}

export default function ImageUploader({
  songId,
  images,
  onImagesChange,
}: ImageUploaderProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);

  if (songId === null) {
    return (
      <div className="border-2 border-dashed border-warm-300 rounded-xl p-6 text-center text-warm-400 text-sm">
        请先保存歌曲基本信息，再上传图片
      </div>
    );
  }

  async function uploadFile(file: File) {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("songId", String(songId));
    const res = await fetch("/api/upload/image", {
      method: "POST",
      body: formData,
    });
    if (!res.ok) throw new Error("Upload failed");
    return res.json() as Promise<Omit<SongImage, "songId">>;
  }

  async function handleFiles(files: FileList | File[]) {
    const accepted = Array.from(files).filter((f) =>
      ["image/jpeg", "image/png", "image/webp"].includes(f.type)
    );
    if (accepted.length === 0) return;
    setUploading(true);
    try {
      const results: SongImage[] = [];
      for (const file of accepted) {
        const item = await uploadFile(file);
        results.push({ ...item, songId: songId! });
      }
      onImagesChange([...images, ...results]);
    } catch (e) {
      console.error(e);
    } finally {
      setUploading(false);
    }
  }

  function moveUp(index: number) {
    if (index === 0) return;
    const next = images.map((img, i) => {
      if (i === index - 1) return { ...images[index], sortOrder: images[index - 1].sortOrder };
      if (i === index) return { ...images[index - 1], sortOrder: images[index].sortOrder };
      return img;
    });
    const swapped = [...next];
    [swapped[index - 1], swapped[index]] = [swapped[index], swapped[index - 1]];
    onImagesChange(swapped);
  }

  function moveDown(index: number) {
    if (index === images.length - 1) return;
    const next = images.map((img, i) => {
      if (i === index) return { ...images[index + 1], sortOrder: images[index].sortOrder };
      if (i === index + 1) return { ...images[index], sortOrder: images[index + 1].sortOrder };
      return img;
    });
    const swapped = [...next];
    [swapped[index], swapped[index + 1]] = [swapped[index + 1], swapped[index]];
    onImagesChange(swapped);
  }

  function remove(index: number) {
    onImagesChange(images.filter((_, i) => i !== index));
  }

  return (
    <div className="space-y-3">
      {/* Drop zone */}
      <div
        className={`border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-colors ${
          dragging
            ? "border-warm-400 bg-warm-100"
            : "border-warm-300 hover:border-warm-400 hover:bg-warm-50"
        }`}
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          handleFiles(e.dataTransfer.files);
        }}
      >
        <input
          ref={inputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp"
          multiple
          className="hidden"
          onChange={(e) => e.target.files && handleFiles(e.target.files)}
        />
        {uploading ? (
          <p className="text-warm-400 text-sm">上传中...</p>
        ) : (
          <p className="text-warm-400 text-sm">
            点击或拖拽图片到此处上传（jpg / png / webp）
          </p>
        )}
      </div>

      {/* Thumbnails */}
      {images.length > 0 && (
        <div className="flex flex-wrap gap-3">
          {images.map((img, index) => (
            <div key={img.id} className="relative group">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={`/api/files/${img.path}`}
                alt={`图片 ${index + 1}`}
                className="w-20 h-20 object-cover rounded-lg border border-warm-200"
              />
              {/* Controls overlay */}
              <div className="absolute inset-0 bg-black/40 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center gap-1">
                <div className="flex gap-1">
                  <button
                    type="button"
                    onClick={() => moveUp(index)}
                    disabled={index === 0}
                    className="w-6 h-6 bg-white/80 rounded text-xs disabled:opacity-30 hover:bg-white"
                    title="上移"
                  >
                    ↑
                  </button>
                  <button
                    type="button"
                    onClick={() => moveDown(index)}
                    disabled={index === images.length - 1}
                    className="w-6 h-6 bg-white/80 rounded text-xs disabled:opacity-30 hover:bg-white"
                    title="下移"
                  >
                    ↓
                  </button>
                </div>
                <button
                  type="button"
                  onClick={() => remove(index)}
                  className="w-6 h-6 bg-red-500/80 rounded text-white text-xs hover:bg-red-600"
                  title="删除"
                >
                  ✕
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
