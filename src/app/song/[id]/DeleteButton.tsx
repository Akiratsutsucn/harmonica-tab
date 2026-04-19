"use client";

import { useRouter } from "next/navigation";

interface DeleteButtonProps {
  songId: number;
}

export default function DeleteButton({ songId }: DeleteButtonProps) {
  const router = useRouter();

  async function handleDelete() {
    if (!confirm("确定要删除这首曲子吗？")) return;
    const res = await fetch(`/api/songs/${songId}`, { method: "DELETE" });
    if (res.ok) {
      router.push("/");
    } else {
      alert("删除失败，请重试");
    }
  }

  return (
    <button
      onClick={handleDelete}
      className="w-9 h-9 flex items-center justify-center rounded-lg text-red-500 hover:bg-red-50"
      aria-label="删除"
    >
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="3 6 5 6 21 6" />
        <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />
        <path d="M10 11v6" />
        <path d="M14 11v6" />
        <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2" />
      </svg>
    </button>
  );
}
