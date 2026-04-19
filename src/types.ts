export interface Song {
  id: number;
  title: string;
  artist: string | null;
  audioType: "file" | "url" | null;
  audioPath: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface SongImage {
  id: number;
  songId: number;
  path: string;
  sortOrder: number;
}

export interface SongWithImages extends Song {
  images: SongImage[];
}
