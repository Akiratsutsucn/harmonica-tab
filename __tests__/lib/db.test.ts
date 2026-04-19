import Database from "better-sqlite3";
import {
  initDb,
  createSong,
  getSong,
  listSongs,
  updateSong,
  deleteSong,
  addImage,
  getImagesBySong,
  deleteImagesBySong,
  deleteImage,
  reorderImages,
} from "@/lib/db";

function makeDb() {
  const db = new Database(":memory:");
  initDb(db);
  return db;
}

describe("songs CRUD", () => {
  test("createSong returns id, getSong retrieves it", () => {
    const db = makeDb();
    const id = createSong(db, { title: "星星", artist: "久石让" });
    expect(typeof id).toBe("number");
    expect(id).toBeGreaterThan(0);

    const song = getSong(db, id);
    expect(song).toBeDefined();
    expect(song!.title).toBe("星星");
    expect(song!.artist).toBe("久石让");
    expect(song!.audioType).toBeNull();
    expect(song!.audioPath).toBeNull();
    expect(song!.createdAt).toBeTruthy();
    expect(song!.updatedAt).toBeTruthy();
  });

  test("getSong returns undefined for missing id", () => {
    const db = makeDb();
    expect(getSong(db, 9999)).toBeUndefined();
  });

  test("listSongs returns all songs", () => {
    const db = makeDb();
    createSong(db, { title: "星星", artist: "久石让" });
    createSong(db, { title: "天空之城", artist: "久石让" });
    const songs = listSongs(db);
    expect(songs).toHaveLength(2);
  });

  test("listSongs filters by title", () => {
    const db = makeDb();
    createSong(db, { title: "星星", artist: "久石让" });
    createSong(db, { title: "天空之城", artist: "久石让" });
    const results = listSongs(db, "星星");
    expect(results).toHaveLength(1);
    expect(results[0].title).toBe("星星");
  });

  test("listSongs filters by artist", () => {
    const db = makeDb();
    createSong(db, { title: "星星", artist: "久石让" });
    createSong(db, { title: "月亮代表我的心", artist: "邓丽君" });
    const results = listSongs(db, "久石");
    expect(results).toHaveLength(1);
    expect(results[0].artist).toBe("久石让");
  });

  test("updateSong changes fields and preserves others", () => {
    const db = makeDb();
    const id = createSong(db, { title: "星星", artist: "久石让" });
    updateSong(db, id, { title: "新星星" });
    const song = getSong(db, id);
    expect(song!.title).toBe("新星星");
    expect(song!.artist).toBe("久石让");
  });

  test("deleteSong removes the song", () => {
    const db = makeDb();
    const id = createSong(db, { title: "星星", artist: "久石让" });
    deleteSong(db, id);
    expect(getSong(db, id)).toBeUndefined();
  });
});

describe("images CRUD", () => {
  test("addImage and getImagesBySong returns images sorted by sortOrder", () => {
    const db = makeDb();
    const songId = createSong(db, { title: "星星" });
    const id1 = addImage(db, { songId, path: "/img/b.jpg", sortOrder: 2 });
    const id2 = addImage(db, { songId, path: "/img/a.jpg", sortOrder: 1 });
    expect(typeof id1).toBe("number");
    expect(typeof id2).toBe("number");

    const images = getImagesBySong(db, songId);
    expect(images).toHaveLength(2);
    expect(images[0].sortOrder).toBe(1);
    expect(images[1].sortOrder).toBe(2);
    expect(images[0].path).toBe("/img/a.jpg");
  });

  test("deleting a song cascade-deletes its images", () => {
    const db = makeDb();
    const songId = createSong(db, { title: "星星" });
    addImage(db, { songId, path: "/img/a.jpg", sortOrder: 0 });
    addImage(db, { songId, path: "/img/b.jpg", sortOrder: 1 });
    deleteSong(db, songId);
    const images = getImagesBySong(db, songId);
    expect(images).toHaveLength(0);
  });

  test("deleteImagesBySong removes all images for a song", () => {
    const db = makeDb();
    const songId = createSong(db, { title: "星星" });
    addImage(db, { songId, path: "/img/a.jpg", sortOrder: 0 });
    deleteImagesBySong(db, songId);
    expect(getImagesBySong(db, songId)).toHaveLength(0);
  });

  test("deleteImage removes single image and returns its path", () => {
    const db = makeDb();
    const songId = createSong(db, { title: "星星" });
    const imgId = addImage(db, { songId, path: "/img/a.jpg", sortOrder: 0 });
    const removedPath = deleteImage(db, imgId);
    expect(removedPath).toBe("/img/a.jpg");
    expect(getImagesBySong(db, songId)).toHaveLength(0);
  });

  test("deleteImage returns undefined for missing id", () => {
    const db = makeDb();
    expect(deleteImage(db, 9999)).toBeUndefined();
  });

  test("reorderImages swaps sortOrder values", () => {
    const db = makeDb();
    const songId = createSong(db, { title: "星星" });
    const id1 = addImage(db, { songId, path: "/img/a.jpg", sortOrder: 0 });
    const id2 = addImage(db, { songId, path: "/img/b.jpg", sortOrder: 1 });

    reorderImages(db, [
      { id: id1, sortOrder: 1 },
      { id: id2, sortOrder: 0 },
    ]);

    const images = getImagesBySong(db, songId);
    expect(images[0].path).toBe("/img/b.jpg");
    expect(images[1].path).toBe("/img/a.jpg");
  });
});
