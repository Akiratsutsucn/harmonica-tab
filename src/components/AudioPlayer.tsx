"use client";

import { useRef, useState, useEffect } from "react";

interface AudioPlayerProps {
  audioType: "file" | "url" | null;
  audioPath: string | null;
}

const SPEEDS = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0];

function formatTime(seconds: number): string {
  if (!isFinite(seconds) || isNaN(seconds)) return "0:00";
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

export default function AudioPlayer({ audioType, audioPath }: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [speedIndex, setSpeedIndex] = useState(2); // default 1.0x

  const src =
    audioType === "file" && audioPath
      ? `/api/files/${audioPath}`
      : audioType === "url" && audioPath
      ? audioPath
      : null;

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const onTimeUpdate = () => setCurrentTime(audio.currentTime);
    const onLoaded = () => setDuration(audio.duration);
    const onEnded = () => setIsPlaying(false);

    audio.addEventListener("timeupdate", onTimeUpdate);
    audio.addEventListener("loadedmetadata", onLoaded);
    audio.addEventListener("ended", onEnded);

    return () => {
      audio.removeEventListener("timeupdate", onTimeUpdate);
      audio.removeEventListener("loadedmetadata", onLoaded);
      audio.removeEventListener("ended", onEnded);
    };
  }, [src]);

  function togglePlay() {
    const audio = audioRef.current;
    if (!audio) return;
    if (isPlaying) {
      audio.pause();
      setIsPlaying(false);
    } else {
      audio.play();
      setIsPlaying(true);
    }
  }

  function handleSeek(e: React.ChangeEvent<HTMLInputElement>) {
    const audio = audioRef.current;
    if (!audio) return;
    const t = Number(e.target.value);
    audio.currentTime = t;
    setCurrentTime(t);
  }

  function cycleSpeed() {
    const audio = audioRef.current;
    const next = (speedIndex + 1) % SPEEDS.length;
    setSpeedIndex(next);
    if (audio) audio.playbackRate = SPEEDS[next];
  }

  if (!src) {
    return (
      <div className="fixed bottom-0 left-0 right-0 h-16 bg-warm-800 flex items-center justify-center z-10">
        <span className="text-warm-400 text-sm">暂无音频</span>
      </div>
    );
  }

  return (
    <div className="fixed bottom-0 left-0 right-0 h-16 bg-warm-800 flex items-center gap-3 px-4 z-10">
      {/* Hidden audio element */}
      <audio ref={audioRef} src={src} preload="metadata" />

      {/* Play/Pause */}
      <button
        onClick={togglePlay}
        className="w-11 h-11 rounded-full bg-warm-400 flex items-center justify-center flex-shrink-0 text-white"
        aria-label={isPlaying ? "暂停" : "播放"}
      >
        {isPlaying ? (
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
            <rect x="6" y="4" width="4" height="16" />
            <rect x="14" y="4" width="4" height="16" />
          </svg>
        ) : (
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
            <polygon points="5,3 19,12 5,21" />
          </svg>
        )}
      </button>

      {/* Time + Progress */}
      <div className="flex-1 flex flex-col gap-1 min-w-0">
        <input
          type="range"
          min={0}
          max={duration || 0}
          step={0.1}
          value={currentTime}
          onChange={handleSeek}
          className="w-full h-1.5 rounded-full appearance-none cursor-pointer"
          style={{
            background: `linear-gradient(to right, var(--color-warm-400) ${duration ? (currentTime / duration) * 100 : 0}%, var(--color-warm-700) 0%)`,
          }}
        />
        <div className="flex justify-between text-xs text-warm-300">
          <span>{formatTime(currentTime)}</span>
          <span>{formatTime(duration)}</span>
        </div>
      </div>

      {/* Speed */}
      <button
        onClick={cycleSpeed}
        className="flex-shrink-0 px-2 py-1 bg-warm-700 text-warm-300 text-xs rounded-lg"
        aria-label="播放速度"
      >
        {SPEEDS[speedIndex]}x
      </button>
    </div>
  );
}
