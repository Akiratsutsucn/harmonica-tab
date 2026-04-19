"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import ImageUploader from "./ImageUploader";
import type { SongWithImages, SongImage } from "@/types";

interface SongFormProps {
  mode: "add" | "edit";
  initialData?: SongWithImages;
}

type AudioMode = "file" | "url";

export default function SongForm({ mode, initialData }: SongFormProps) {
  const router = useRouter();

  const [title, setTitle] = useState(initialData?.title ?? "");
  const [artist, setArtist] = useState(initialData?.artist ?? "");
  const [audioMode, setAudioMode] = useState<AudioMode>(
    initialData?.audioType === "url" ? "url" : "file"
  );
  const [audioFile, setAudioFile] = useState<File | null>(null);
  const [audioUrl, setAudioUrl] = useState(
    initialData?.audioType === "url" ? (initialData.audioPath ?? "") : ""
  );
  const [imageFiles, setImageFiles] = useState<File[]>([]);
  const [imagePreviews, setImagePreviews] = useState<string[]>([]);
  const [images, setImages] = useState<SongImage[]>(initialData?.images ?? []);
  const [songId, setSongId] = useState<number | null>(initialData?.id ?? null);
  const [saved, setSaved] = useState(mode === "edit");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function handleImageSelect(files: FileList | null) {
    if (!files) return;
    const accepted = Array.from(files).filter((f) =>
      ["image/jpeg", "image/png", "image/webp"].includes(f.type)
    );
    if (accepted.length === 0) return;
    setImageFiles((prev) => [...prev, ...accepted]);
    const newPreviews = accepted.map((f) => URL.createObjectURL(f));
    setImagePreviews((prev) => [...prev, ...newPreviews]);
  }

  function removeImagePreview(index: number) {
    URL.revokeObjectURL(imagePreviews[index]);
    setImageFiles((prev) => prev.filter((_, i) => i !== index));
    setImagePreviews((prev) => prev.filter((_, i) => i !== index));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim()) {
      setError("请填写歌曲名称");
      return;
    }
    setError(null);
    setSubmitting(true);

    try {
      let id: number;

      if (mode === "add") {
        // Step 1: create song
        const res = await fetch("/api/songs", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ title: title.trim(), artist: artist.trim() || undefined }),
        });
        if (!res.ok) throw new Error("创建歌曲失败");
        const song: SongWithImages = await res.json();
        id = song.id;
        setSongId(id);

        // Step 2: handle audio
        if (audioMode === "file" && audioFile) {
          const fd = new FormData();
          fd.append("file", audioFile);
          fd.append("songId", String(id));
          const audioRes = await fetch("/api/upload/audio", { method: "POST", body: fd });
          if (!audioRes.ok) throw new Error("音频上传失败");
        } else if (audioMode === "url" && audioUrl.trim()) {
          const putRes = await fetch(`/api/songs/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ audioType: "url", audioPath: audioUrl.trim() }),
          });
          if (!putRes.ok) throw new Error("保存音频链接失败");
        }

        // Step 3: upload images
        for (const file of imageFiles) {
          const fd = new FormData();
          fd.append("file", file);
          fd.append("songId", String(id));
          const imgRes = await fetch("/api/upload/image", { method: "POST", body: fd });
          if (!imgRes.ok) throw new Error("图片上传失败");
        }

        router.push(`/song/${id}`);
      } else {
        // Edit mode
        id = initialData!.id;
        const putRes = await fetch(`/api/songs/${id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            title: title.trim(),
            artist: artist.trim() || null,
          }),
        });
        if (!putRes.ok) throw new Error("更新歌曲失败");

        if (audioMode === "file" && audioFile) {
          const fd = new FormData();
          fd.append("file", audioFile);
          fd.append("songId", String(id));
          const audioRes = await fetch("/api/upload/audio", { method: "POST", body: fd });
          if (!audioRes.ok) throw new Error("音频上传失败");
        } else if (audioMode === "url" && audioUrl.trim()) {
          const putAudioRes = await fetch(`/api/songs/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ audioType: "url", audioPath: audioUrl.trim() }),
          });
          if (!putAudioRes.ok) throw new Error("保存音频链接失败");
        }

        router.push(`/song/${id}`);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "操作失败");
    } finally {
      setSubmitting(false);
    }
  }

  function handleDone() {
    if (songId) router.push(`/song/${songId}`);
  }

  const inputClass =
    "w-full border border-warm-200 rounded-lg px-3 py-2 text-warm-800 bg-white placeholder:text-warm-300 focus:outline-none focus:ring-2 focus:ring-warm-300 focus:border-warm-400";

  return (
    <div className="px-4 py-6 max-w-2xl mx-auto">
      {!saved ? (
        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-warm-700 mb-1">
              歌曲名称 <span className="text-red-400">*</span>
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="歌曲名称"
              className={inputClass}
              required
            />
          </div>

          {/* Artist */}
          <div>
            <label className="block text-sm font-medium text-warm-700 mb-1">
              歌手 / 作曲家
            </label>
            <input
              type="text"
              value={artist}
              onChange={(e) => setArtist(e.target.value)}
              placeholder="歌手/作曲家"
              className={inputClass}
            />
          </div>

          {/* Audio source */}
          <div>
            <label className="block text-sm font-medium text-warm-700 mb-2">
              音频来源
            </label>
            <div className="flex gap-2 mb-3">
              {(["file", "url"] as AudioMode[]).map((m) => (
                <button
                  key={m}
                  type="button"
                  onClick={() => setAudioMode(m)}
                  className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
                    audioMode === m
                      ? "bg-warm-400 text-white"
                      : "bg-warm-100 text-warm-600 hover:bg-warm-200"
                  }`}
                >
                  {m === "file" ? "上传文件" : "填写链接"}
                </button>
              ))}
            </div>
            {audioMode === "file" ? (
              <input
                type="file"
                accept="audio/*,.mp3,.wav,.m4a,.ogg"
                onChange={(e) => setAudioFile(e.target.files?.[0] ?? null)}
                className="block w-full text-sm text-warm-600 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:bg-warm-100 file:text-warm-700 hover:file:bg-warm-200"
              />
            ) : (
              <input
                type="url"
                value={audioUrl}
                onChange={(e) => setAudioUrl(e.target.value)}
                placeholder="音频链接地址"
                className={inputClass}
              />
            )}
          </div>

          {/* Images (add mode) */}
          {mode === "add" && (
            <div>
              <label className="block text-sm font-medium text-warm-700 mb-2">
                乐谱图片
              </label>
              <input
                type="file"
                accept="image/jpeg,image/png,image/webp"
                multiple
                onChange={(e) => handleImageSelect(e.target.files)}
                className="block w-full text-sm text-warm-600 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:bg-warm-100 file:text-warm-700 hover:file:bg-warm-200"
              />
              {imagePreviews.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-2">
                  {imagePreviews.map((src, i) => (
                    <div key={i} className="relative group">
                      {/* eslint-disable-next-line @next/next/no-img-element */}
                      <img src={src} alt={`预览 ${i + 1}`} className="w-16 h-16 object-cover rounded-lg border border-warm-200" />
                      <button
                        type="button"
                        onClick={() => removeImagePreview(i)}
                        className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white rounded-full text-xs leading-none flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                      >
                        ✕
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {error && (
            <p className="text-red-500 text-sm">{error}</p>
          )}

          <button
            type="submit"
            disabled={submitting}
            className="w-full bg-warm-400 text-white py-2.5 rounded-xl font-semibold hover:bg-warm-500 transition-colors disabled:opacity-60"
          >
            {submitting ? "保存中..." : "保存"}
          </button>
        </form>
      ) : (
        <div className="space-y-5">
          {/* Saved confirmation */}
          <div className="bg-green-50 border border-green-200 rounded-xl px-4 py-3 text-green-700 text-sm">
            ✓ 保存成功！现在可以上传乐谱图片。
          </div>

          {/* Image uploader */}
          <div>
            <label className="block text-sm font-medium text-warm-700 mb-2">
              乐谱图片
            </label>
            <ImageUploader
              songId={songId}
              images={images}
              onImagesChange={setImages}
            />
          </div>

          <button
            type="button"
            onClick={handleDone}
            className="w-full bg-warm-400 text-white py-2.5 rounded-xl font-semibold hover:bg-warm-500 transition-colors"
          >
            完成
          </button>
        </div>
      )}
    </div>
  );
}
