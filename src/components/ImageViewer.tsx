"use client";

import { Swiper, SwiperSlide } from "swiper/react";
import { Zoom, Pagination } from "swiper/modules";
import type { SongImage } from "@/types";

import "swiper/css";
import "swiper/css/zoom";
import "swiper/css/pagination";

interface ImageViewerProps {
  images: SongImage[];
}

export default function ImageViewer({ images }: ImageViewerProps) {
  if (images.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-warm-400 text-base">
        暂无简谱图片
      </div>
    );
  }

  return (
    <Swiper
      modules={[Zoom, Pagination]}
      zoom={{ maxRatio: 4 }}
      pagination={{ clickable: true }}
      className="h-full w-full"
    >
      {images.map((image) => (
        <SwiperSlide key={image.id} className="flex items-center justify-center">
          <div className="swiper-zoom-container">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={`/api/files/${image.path}`}
              alt={`简谱第${image.sortOrder + 1}页`}
              className="max-h-full max-w-full object-contain"
            />
          </div>
        </SwiperSlide>
      ))}
    </Swiper>
  );
}
