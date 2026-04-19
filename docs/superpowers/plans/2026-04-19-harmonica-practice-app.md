# 口琴练习 APP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a personal harmonica practice app where users upload sheet music images and audio to practice alongside.

**Architecture:** Next.js 14 full-stack app with App Router. SQLite (better-sqlite3) for metadata, disk storage for uploaded files. Single deployment on Ubuntu server with PM2.

**Tech Stack:** Next.js 14, TypeScript, Tailwind CSS, better-sqlite3, Swiper (image carousel + zoom), Vitest (testing)

---

## File Structure

```
harmonica-app/
├── src/
│   ├── app/
│   │   ├── layout.tsx                    # Root layout, warm theme, system font
│   │   ├── page.tsx                      # Home — song list with search
│   │   ├── add/
│   │   │   └── page.tsx                  # Add song form
│   │   ├── song/
│   │   │   └── [id]/
│   │   │       ├── page.tsx              # Practice page
│   │   │       └── edit/
│   │   │           └── page.tsx          # Edit song
│   │   └── api/
│   │       ├── songs/
│   │       │   ├── route.ts              # GET list, POST create
│   │       │   └── [id]/
│   │       │       └── route.ts          # GET detail, PUT update, DELETE
│   │       └── upload/
│   │           ├── image/
│   │           │   └── route.ts          # POST upload image
│   │           └── audio/
│   │               └── route.ts          # POST upload audio
│   ├── lib/
│   │   └── db.ts                         # SQLite init, schema, query helpers
│   ├── components/
│   │   ├── SongCard.tsx                  # Card for song list
│   │   ├── AudioPlayer.tsx               # Fixed bottom player
│   │   ├── ImageViewer.tsx               # Swiper carousel + zoom
│   │   ├── SongForm.tsx                  # Shared add/edit form
│   │   └── ImageUploader.tsx             # Multi-image upload + reorder
│   └── types.ts                          # Shared TypeScript types
├── uploads/                              # User uploads (gitignored)
│   ├── images/
│   └── audio/
├── __tests__/
│   ├── lib/
│   │   └── db.test.ts                    # DB layer tests
│   └── api/
│       ├── songs.test.ts                 # Songs CRUD API tests
│       └── upload.test.ts                # Upload API tests
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── package.json
├── vitest.config.ts
├── ecosystem.config.js                   # PM2 config
└── .gitignore
```

---

### Task 1: Project Scaffold

**Goal:** Clear old code, create Next.js 14 project, configure Tailwind warm theme.

**Files:**
- Delete: `backend/`, `frontend/`, `import_batch.py`, `new_songs_batch.py`
- Create: Next.js project files via `create-next-app`
- Create: `src/types.ts`
- Modify: `tailwind.config.ts` (warm theme)
- Modify: `src/app/layout.tsx` (warm background)
- Modify: `.gitignore` (add uploads/)

- [ ] **Step 1: Remove old project files**

```bash
cd E:/Workspace/claude/harmonica-app
rm -rf backend/ frontend/ import_batch.py new_songs_batch.py __pycache__/
```

- [ ] **Step 2: Initialize Next.js project**

```bash
cd E:/Workspace/claude/harmonica-app
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --no-import-alias --use-npm
```

When prompted about overwriting files, accept. This creates the Next.js scaffold in the current directory.

- [ ] **Step 3: Update .gitignore**

Add to `.gitignore`:
```
uploads/
*.db
.superpowers/
```

- [ ] **Step 4: Configure Tailwind warm theme**

Edit `tailwind.config.ts`:
```typescript
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        warm: {
          50: "#faf6f0",
          100: "#f0e8d8",
          200: "#e0d5c5",
          300: "#c4a882",
          400: "#a67c2e",
          500: "#8b6914",
          600: "#6b5010",
          700: "#4a370b",
          800: "#3a2e1a",
          900: "#2a1f0f",
        },
      },
    },
  },
  plugins: [],
};
export default config;
```

- [ ] **Step 5: Set up root layout with warm theme**

Edit `src/app/layout.tsx`:
```tsx
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "口琴练习",
  description: "个人口琴练习工具 — 边看谱边听歌",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className="bg-warm-50 text-warm-800 min-h-screen antialiased">
        {children}
      </body>
    </html>
  );
}
```

- [ ] **Step 6: Set up global CSS**

Replace `src/app/globals.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, "Noto Sans SC", sans-serif;
}
```

- [ ] **Step 7: Create shared types**

Create `src/types.ts`:
```typescript
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
```

- [ ] **Step 8: Create placeholder home page**

Replace `src/app/page.tsx`:
```tsx
export default function Home() {
  return (
    <main className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-warm-500">🎵 口琴练习</h1>
      <p className="text-warm-300 mt-2">我的曲库</p>
    </main>
  );
}
```

- [ ] **Step 9: Verify dev server starts**

Run: `npm run dev`
Expected: App loads at http://localhost:3000 with warm background and "口琴练习" heading.

- [ ] **Step 10: Commit**

```bash
git add -A
git commit -m "feat: scaffold Next.js 14 project with warm theme"
```

---

### Task 2: Database Layer

**Goal:** SQLite database with songs and images tables, CRUD query helpers, tests.

**Files:**
- Create: `src/lib/db.ts`
- Create: `__tests__/lib/db.test.ts`
- Create: `vitest.config.ts`
- Modify: `package.json` (add dependencies)

- [ ] **Step 1: Install dependencies**

```bash
npm install better-sqlite3
npm install -D @types/better-sqlite3 vitest
```

- [ ] **Step 2: Create vitest config**

Create `vitest.config.ts` with globals: true, environment: node, and path alias `@` -> `./src`.

Add to `package.json` scripts: `"test": "vitest run"`, `"test:watch": "vitest"`.

- [ ] **Step 3: Write failing DB tests**

Create `__tests__/lib/db.test.ts`. Use in-memory SQLite for isolation. Each test creates a fresh DB via `new Database(":memory:")` + `initDb(db)`.

Key test cases:
- `createSong` returns id, `getSong` retrieves it with correct fields
- `listSongs` returns all songs; `listSongs(db, "xingxing")` filters by title; `listSongs(db, "jiushi")` filters by artist
- `updateSong` changes fields and preserves others
- `deleteSong` removes the song, `getSong` returns undefined
- `addImage` + `getImagesBySong` returns images sorted by sortOrder
- Deleting a song cascade-deletes its images
- `reorderImages` swaps sortOrder values

- [ ] **Step 4: Run tests to verify they fail**

Run: `npx vitest run`
Expected: FAIL - module `@/lib/db` not found.

- [ ] **Step 5: Implement database layer**

Create `src/lib/db.ts` with:
- `getDb()` - singleton that opens `harmonica.db` in project root, enables WAL + foreign keys, calls `initDb`
- `initDb(db)` - creates songs and images tables if not exist (songs: id, title, artist, audioType, audioPath, createdAt, updatedAt; images: id, songId FK CASCADE, path, sortOrder)
- `createSong(db, {title, artist, audioType?, audioPath?})` returns id
- `getSong(db, id)` returns song row or undefined
- `listSongs(db, search?)` returns array, ordered by updatedAt DESC, LIKE search on title/artist
- `updateSong(db, id, {title?, artist?, audioType?, audioPath?})` dynamic SET clause, updates updatedAt
- `deleteSong(db, id)` DELETE, cascade handles images
- `addImage(db, {songId, path, sortOrder})` returns id
- `getImagesBySong(db, songId)` returns array ordered by sortOrder ASC
- `deleteImagesBySong(db, songId)` DELETE all images for song
- `reorderImages(db, [{id, sortOrder}])` transaction, batch UPDATE sortOrder

- [ ] **Step 6: Run tests to verify they pass**

Run: `npx vitest run`
Expected: All 6 tests PASS.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat: database layer with SQLite schema and CRUD helpers"
```

---

### Task 3: Songs CRUD API Routes

**Goal:** REST API for songs with list, create, detail, update, delete.

**Files:**
- Create: `src/app/api/songs/route.ts`
- Create: `src/app/api/songs/[id]/route.ts`

- [ ] **Step 1: Implement songs list + create route**

Create `src/app/api/songs/route.ts`:
- `GET /api/songs?q=search` - calls `listSongs(getDb(), q)`, returns JSON array. Each song includes its images via `getImagesBySong`.
- `POST /api/songs` - accepts JSON body `{title, artist?, audioType?, audioPath?}`, validates title is non-empty, calls `createSong`, returns created song with 201 status.

- [ ] **Step 2: Implement song detail + update + delete route**

Create `src/app/api/songs/[id]/route.ts`:
- `GET /api/songs/[id]` - calls `getSong`, returns 404 if not found, otherwise returns song with images.
- `PUT /api/songs/[id]` - accepts JSON body with optional fields, calls `updateSong`, returns updated song.
- `DELETE /api/songs/[id]` - calls `deleteSong`, also deletes upload files from disk (`uploads/images/{id}/` and `uploads/audio/{id}/`), returns 204.

- [ ] **Step 3: Verify API manually**

Run: `npm run dev`
Test with curl:
```bash
# Create
curl -X POST http://localhost:3000/api/songs -H "Content-Type: application/json" -d "{\"title\":\"Test Song\",\"artist\":\"Test\"}"
# List
curl http://localhost:3000/api/songs
# Get
curl http://localhost:3000/api/songs/1
# Update
curl -X PUT http://localhost:3000/api/songs/1 -H "Content-Type: application/json" -d "{\"title\":\"Updated\"}"
# Delete
curl -X DELETE http://localhost:3000/api/songs/1
```

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat: songs CRUD API routes"
```

---

### Task 4: File Upload API + Static Serving

**Goal:** Upload image and audio files, serve them statically, delete them.

**Files:**
- Create: `src/app/api/upload/image/route.ts`
- Create: `src/app/api/upload/audio/route.ts`
- Create: `src/app/api/files/[...path]/route.ts`
- Modify: `next.config.ts` (if needed for file size limits)

- [ ] **Step 1: Implement image upload route**

Create `src/app/api/upload/image/route.ts`:
- `POST /api/upload/image` - accepts multipart form data with `file` field and `songId` field.
- Validates file is image (jpg/png/webp).
- Saves to `uploads/images/{songId}/{uuid}.{ext}`.
- Creates directory if not exists.
- Calls `addImage(db, {songId, path, sortOrder})` where sortOrder = current max + 1.
- Returns `{id, path, sortOrder}` with 201.

Use `crypto.randomUUID()` for filenames. Use `Request.formData()` for parsing (no extra library needed in Next.js 14).

- [ ] **Step 2: Implement audio upload route**

Create `src/app/api/upload/audio/route.ts`:
- `POST /api/upload/audio` - accepts multipart form data with `file` field and `songId` field.
- Validates file is audio (mp3, wav, m4a, ogg).
- Saves to `uploads/audio/{songId}/{uuid}.{ext}`.
- Calls `updateSong(db, songId, {audioType: "file", audioPath: relative_path})`.
- Returns `{audioType: "file", audioPath}` with 201.

- [ ] **Step 3: Implement static file serving**

Create `src/app/api/files/[...path]/route.ts`:
- `GET /api/files/images/1/abc.jpg` - reads file from `uploads/images/1/abc.jpg`, returns with correct Content-Type.
- Maps extensions to MIME types: jpg/jpeg -> image/jpeg, png -> image/png, webp -> image/webp, mp3 -> audio/mpeg, wav -> audio/wav, m4a -> audio/mp4, ogg -> audio/ogg.
- Returns 404 if file not found.
- Sanitize path to prevent directory traversal (reject paths with `..`).

- [ ] **Step 4: Configure Next.js for large uploads**

Modify `next.config.ts` to set body size limit:
```typescript
const nextConfig = {
  experimental: {
    serverActions: {
      bodySizeLimit: "50mb",
    },
  },
  // Disable body parser for API routes that handle file uploads
  api: {
    bodyParser: false,
  },
};
```

Also export route segment config in upload routes:
```typescript
export const runtime = "nodejs";
export const dynamic = "force-dynamic";
```

- [ ] **Step 5: Verify uploads manually**

Run: `npm run dev`
Test image upload with curl:
```bash
curl -X POST http://localhost:3000/api/upload/image -F "file=@test.jpg" -F "songId=1"
```
Then verify the file is accessible at the returned path via `/api/files/...`.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "feat: file upload API and static file serving"
```

---

### Task 5: Home Page - Song List with Search

**Goal:** Home page showing song cards with search, floating add button.

**Files:**
- Create: `src/components/SongCard.tsx`
- Modify: `src/app/page.tsx`

- [ ] **Step 1: Create SongCard component**

Create `src/components/SongCard.tsx`:
- Client component (`"use client"`)
- Props: `song: SongWithImages`
- Displays: first image as thumbnail (or music note emoji placeholder), title, artist
- Warm card style: white bg, rounded-xl, shadow-sm, hover shadow-md transition
- Thumbnail: 64x64 rounded-lg, object-cover
- Clicking the card navigates to `/song/{id}` using `useRouter`

- [ ] **Step 2: Build home page**

Modify `src/app/page.tsx`:
- Server component that fetches songs from DB directly (no API call needed for server components)
- Header: app title with music note icon, song count
- Search bar: controlled input, filters client-side (or use URL search params for server-side)
- Song list: maps songs to SongCard components
- Empty state: friendly message when no songs exist
- Floating add button: fixed bottom-right, circular, warm-400 bg, links to `/add`
- Use `getDb()` + `listSongs()` + `getImagesBySong()` directly in the server component

Actually, for search to work without full page reload, make the song list a client component that fetches from `/api/songs?q=...`. The page itself can be a simple wrapper.

Revised approach:
- `src/app/page.tsx` - minimal server component wrapper
- `src/components/SongList.tsx` - client component with search state, fetches from API, renders SongCards

Create `src/components/SongList.tsx`:
- `"use client"`
- State: `songs[]`, `search string`, `loading boolean`
- On mount and search change: fetch `/api/songs?q={search}` with debounce (300ms)
- Renders search input + SongCard grid + empty state + floating add button

- [ ] **Step 3: Style the warm theme**

Ensure the page looks like the brainstorming mockup:
- Background: bg-warm-50
- Header gradient: from-warm-500 to-warm-400, white text
- Search bar: white bg, warm-200 border, rounded-xl
- Cards: white bg, rounded-xl, shadow with warm tint
- Add button: warm-400 bg, white + icon, rounded-full, shadow-lg

- [ ] **Step 4: Verify in browser**

Run: `npm run dev`
Open http://localhost:3000
Expected: Warm-themed home page with header, search bar, empty state message, floating + button.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: home page with song list and search"
```

---

### Task 6: Add Song Page

**Goal:** Form to create a song with image uploads and audio input.

**Files:**
- Create: `src/components/SongForm.tsx`
- Create: `src/components/ImageUploader.tsx`
- Create: `src/app/add/page.tsx`

- [ ] **Step 1: Create ImageUploader component**

Create `src/components/ImageUploader.tsx`:
- `"use client"`
- Props: `songId: number | null`, `images: {id, path, sortOrder}[]`, `onImagesChange: (images) => void`
- Drop zone: dashed border, click or drag to upload
- Accepts jpg/png/webp, multiple files
- When songId is available, uploads immediately via `POST /api/upload/image`
- Shows thumbnails of uploaded images in a grid
- Each thumbnail has: move up/down buttons (for reorder), delete button (X)
- Reorder calls `onImagesChange` with updated sortOrder

- [ ] **Step 2: Create SongForm component**

Create `src/components/SongForm.tsx`:
- `"use client"`
- Props: `mode: "add" | "edit"`, `initialData?: SongWithImages`, `onSuccess?: (id: number) => void`
- Fields:
  - Title (text input, required)
  - Artist (text input, optional)
  - Audio source toggle: "upload file" | "paste URL"
    - If file: file input accepting audio/*
    - If URL: text input for URL
  - Image uploader (ImageUploader component)
- Submit flow for "add" mode:
  1. POST /api/songs with title + artist -> get song id
  2. If audio file: POST /api/upload/audio with file + songId
  3. If audio URL: PUT /api/songs/{id} with audioType="url", audioPath=url
  4. Images are already uploaded by ImageUploader during interaction
  5. Navigate to /song/{id}
- Submit flow for "edit" mode:
  1. PUT /api/songs/{id} with changed fields
  2. Handle audio changes same as add
  3. Navigate back to /song/{id}

- [ ] **Step 3: Create add page**

Create `src/app/add/page.tsx`:
- Simple wrapper that renders SongForm in "add" mode
- Back button in header linking to /
- Title: "Add Song"

- [ ] **Step 4: Verify in browser**

Run: `npm run dev`
Navigate to http://localhost:3000/add
Expected: Form with title, artist, audio toggle, image uploader. Submit creates a song and redirects.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: add song page with image upload and audio input"
```

---

### Task 7: Practice Page

**Goal:** View sheet music images with swipe/zoom and play audio with speed control.

**Files:**
- Create: `src/components/ImageViewer.tsx`
- Create: `src/components/AudioPlayer.tsx`
- Create: `src/app/song/[id]/page.tsx`

- [ ] **Step 1: Install Swiper**

```bash
npm install swiper
```

- [ ] **Step 2: Create ImageViewer component**

Create `src/components/ImageViewer.tsx`:
- `"use client"`
- Props: `images: SongImage[]`
- Uses Swiper with Zoom and Pagination modules
- Full-width slides, each containing an image
- Pagination dots at bottom of image area
- Zoom: double-tap or pinch on mobile, scroll-wheel on desktop
- Images load from `/api/files/{path}`
- If no images: show placeholder message

- [ ] **Step 3: Create AudioPlayer component**

Create `src/components/AudioPlayer.tsx`:
- `"use client"`
- Props: `audioType: "file" | "url" | null`, `audioPath: string | null`
- Fixed to bottom of viewport, height ~64px, warm dark background (warm-800)
- Uses HTML5 Audio element (hidden), custom UI:
  - Play/pause button (large, circular, warm-400 bg)
  - Progress bar (clickable/draggable, warm-400 fill on warm-700 track)
  - Current time / total duration display
  - Speed button cycling through: 0.5x, 0.75x, 1.0x, 1.25x, 1.5x, 2.0x
- Audio src: if audioType is "file", use `/api/files/{audioPath}`; if "url", use audioPath directly
- If no audio: show "No audio" message in player area
- State: playing, currentTime, duration, playbackRate
- useRef for Audio element, useEffect for event listeners (timeupdate, loadedmetadata, ended)

- [ ] **Step 4: Create practice page**

Create `src/app/song/[id]/page.tsx`:
- Server component that fetches song + images from DB
- Top nav bar: back button (arrow left, links to /), song title, edit button (links to /song/{id}/edit), delete button
- Delete button: shows confirm dialog, then calls DELETE /api/songs/{id}, redirects to /
- Main area: ImageViewer component (takes remaining height minus nav and player)
- Bottom: AudioPlayer component (fixed)
- Layout: flex column, image viewer gets `flex-1 overflow-hidden`, player is fixed bottom with appropriate z-index
- Add bottom padding to image area equal to player height so content is not hidden behind player

- [ ] **Step 5: Verify in browser**

Run: `npm run dev`
1. First add a song via /add with at least one image and audio
2. Navigate to the song practice page
3. Verify: images display and can be swiped, zoom works, audio plays with controls, speed toggle works

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "feat: practice page with image viewer and audio player"
```

---

### Task 8: Edit Song Page

**Goal:** Edit existing song details, images, and audio.

**Files:**
- Create: `src/app/song/[id]/edit/page.tsx`

- [ ] **Step 1: Create edit page**

Create `src/app/song/[id]/edit/page.tsx`:
- Server component that fetches song + images from DB
- If song not found, redirect to /
- Renders SongForm in "edit" mode with initialData
- Header: back button (to /song/{id}), title "Edit Song"
- On success: navigate to /song/{id}

- [ ] **Step 2: Update SongForm for edit mode**

Ensure SongForm handles edit mode:
- Pre-populates all fields from initialData
- ImageUploader shows existing images
- Audio section shows current audio (file name or URL) with option to change
- Submit calls PUT /api/songs/{id} instead of POST

- [ ] **Step 3: Add delete image functionality**

Add to ImageUploader: when deleting an image in edit mode, call the API to remove it from DB and delete the file. Add a `DELETE /api/upload/image/{imageId}` endpoint or handle via song update.

Simpler approach: add `deleteImage` function to `src/lib/db.ts`:
```typescript
export function deleteImage(db: Database.Database, imageId: number): string | undefined {
  const image = db.prepare("SELECT path FROM images WHERE id = ?").get(imageId) as any;
  if (image) {
    db.prepare("DELETE FROM images WHERE id = ?").run(imageId);
    return image.path; // caller deletes file from disk
  }
  return undefined;
}
```

Add API route or handle in the image upload route with DELETE method.

- [ ] **Step 4: Verify in browser**

Run: `npm run dev`
1. Navigate to an existing song, click edit
2. Change title, add/remove images, change audio
3. Save and verify changes persist

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: edit song page"
```

---

### Task 9: Deployment

**Goal:** Deploy to 115.190.112.212:5123 with PM2.

**Files:**
- Create: `ecosystem.config.js`
- Modify: `next.config.ts` (production settings)

- [ ] **Step 1: Create PM2 config**

Create `ecosystem.config.js`:
```javascript
module.exports = {
  apps: [{
    name: "harmonica-app",
    script: "node_modules/.bin/next",
    args: "start -p 5123",
    cwd: "/var/www/harmonica-app",
    env: {
      NODE_ENV: "production",
    },
  }],
};
```

- [ ] **Step 2: Update next.config.ts for production**

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
};

export default nextConfig;
```

- [ ] **Step 3: Push to GitHub**

```bash
git add -A
git commit -m "chore: add PM2 deployment config"
git push origin main
```

- [ ] **Step 4: Deploy to server**

SSH into server and run:
```bash
ssh -i "E:/Workspace/claude/115.190.112.212 SSH Secret.pem" root@115.190.112.212

# On server:
# Stop old service if running
systemctl stop harmonica-tab 2>/dev/null || true
systemctl disable harmonica-tab 2>/dev/null || true

# Clone/pull repo
cd /var/www
rm -rf harmonica-app
git clone git@github.com:Akiratsutsucn/harmonica-tab.git harmonica-app
cd harmonica-app

# Install and build
npm install
npm run build

# Create uploads directory
mkdir -p uploads/images uploads/audio

# Start with PM2
pm2 delete harmonica-app 2>/dev/null || true
pm2 start ecosystem.config.js
pm2 save
```

- [ ] **Step 5: Verify deployment**

Open http://115.190.112.212:5123 in browser.
Expected: App loads with warm theme, can add songs, practice with images and audio.

- [ ] **Step 6: Commit any deployment fixes**

If any fixes were needed during deployment, commit them.

---

## Summary

| Task | Description | Dependencies |
|------|-------------|-------------|
| 1 | Project scaffold + warm theme | None |
| 2 | Database layer + tests | Task 1 |
| 3 | Songs CRUD API | Task 2 |
| 4 | File upload API + static serving | Task 2 |
| 5 | Home page UI | Task 3 |
| 6 | Add song page | Task 3, 4 |
| 7 | Practice page | Task 3, 4 |
| 8 | Edit song page | Task 6, 7 |
| 9 | Deployment | All above |
