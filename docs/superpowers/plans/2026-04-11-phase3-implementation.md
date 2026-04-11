# Phase 3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为口琴简谱学习工具添加 UI 升级（白净风）、播放练习模式（Web Audio + 分段循环 + 调速 + 难度）、jianpu.cn 爬取器、曲库扩充至 30+ 首。

**Architecture:** 前后端同步推进。后端先做 DB 迁移 + schema 更新 + 爬取器重写，前端先做 AudioEngine 核心模块，再做 UI 重写整合所有功能。曲库 seed data 作为独立任务最后合入。

**Tech Stack:** FastAPI, aiosqlite, httpx, BeautifulSoup4, React 19, Vite 8, Web Audio API

---

## File Structure

### 新增文件

| File | Responsibility |
|------|----------------|
| `frontend/src/AudioEngine.js` | Web Audio API 封装：频率计算、播放调度、速度控制 |
| `frontend/src/PlayBar.jsx` | 底部固定播放控制栏：播放/暂停、进度、速度选择 |
| `frontend/src/DifficultyBadge.jsx` | 难度标签组件（入门/初级/中级） |
| `backend/app/seed_songs.py` | 30+ 首曲库 seed data（从 main.py 提取） |

### 修改文件

| File | Changes |
|------|---------|
| `backend/app/database.py` | 新增 difficulty 字段迁移 |
| `backend/app/schemas.py` | SongOut/SongDetail 增加 difficulty |
| `backend/app/routes_songs.py` | 支持 difficulty 筛选参数 |
| `backend/app/main.py` | seed data 引用 seed_songs.py，seed 加 difficulty |
| `backend/app/pipeline/scraper.py` | 重写：jianpu.cn 真实爬取 + 图片 URL 提取 |
| `backend/app/pipeline/parser.py` | 重写：jianpu.cn 搜索结果解析 |
| `frontend/src/index.css` | 全面重写为白净风格 |
| `frontend/src/App.jsx` | 难度筛选、播放集成、新 UI 结构 |
| `frontend/src/JianpuRenderer.jsx` | 播放高亮、分段选择支持、更大字号 |
| `frontend/src/api.js` | 新增 difficulty 筛选参数 |

---

## Task 1: 后端 — DB 迁移 + Schema 更新

**Files:**
- Modify: `backend/app/database.py`
- Modify: `backend/app/schemas.py`
- Modify: `backend/app/routes_songs.py`

- [ ] **Step 1: 修改 database.py — 添加 difficulty 字段迁移**

在 `init_db()` 末尾的迁移区域添加：

```python
# Migrate: add difficulty column if missing
try:
    await db.execute("SELECT difficulty FROM songs LIMIT 1")
except Exception:
    await db.execute("ALTER TABLE songs ADD COLUMN difficulty INTEGER DEFAULT 1")
```

- [ ] **Step 2: 修改 schemas.py — SongOut 增加 difficulty**

在 `SongOut` 类中添加字段：

```python
class SongOut(SongBase):
    id: int
    source: str = "manual"
    verified: bool = False
    status: str = "verified"
    difficulty: int = 1
```

`SongDetail` 继承 `SongOut`，自动获得 `difficulty`。

- [ ] **Step 3: 修改 routes_songs.py — 支持 difficulty 筛选**

修改 `search_songs` 函数签名，增加 `difficulty` 参数：

```python
@router.get("", response_model=list[SongOut])
async def search_songs(
    q: str = Query("", description="Search by title or artist"),
    difficulty: int | None = Query(None, ge=1, le=3, description="1=入门 2=初级 3=中级"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: aiosqlite.Connection = Depends(get_db),
):
    offset = (page - 1) * limit
    conditions = ["status='verified'"]
    params = []
    if q:
        conditions.append("(title LIKE ? OR artist LIKE ?)")
        params.extend([f"%{q}%", f"%{q}%"])
    if difficulty is not None:
        conditions.append("difficulty = ?")
        params.append(difficulty)
    where = " AND ".join(conditions)
    params.extend([limit, offset])
    rows = await db.execute_fetchall(
        f"SELECT * FROM songs WHERE {where} ORDER BY title LIMIT ? OFFSET ?",
        params,
    )
    return [dict(r) for r in rows]
```

- [ ] **Step 4: 验证后端启动无报错**

Run: `cd backend && python -m uvicorn app.main:app --port 5123`
Expected: 启动成功，无报错

- [ ] **Step 5: Commit**

```bash
git add backend/app/database.py backend/app/schemas.py backend/app/routes_songs.py
git commit -m "feat: add difficulty field to songs table and API"
```

---

## Task 2: 前端 — AudioEngine 核心模块

**Files:**
- Create: `frontend/src/AudioEngine.js`

- [ ] **Step 1: 创建 AudioEngine.js**

```js
/**
 * Web Audio API engine for playing jianpu notes.
 *
 * Usage:
 *   const engine = new AudioEngine();
 *   engine.playSequence(notes, bpm, { speed, onNote, onDone });
 *   engine.stop();
 */

const NOTE_MIDI = {
  C: 0, 'C#': 1, Db: 1, D: 2, 'D#': 3, Eb: 3, E: 4, F: 5,
  'F#': 6, Gb: 6, G: 7, 'G#': 8, Ab: 8, A: 9, 'A#': 10, Bb: 10, B: 11,
};

const DURATION_BEATS = {
  whole: 4, half: 2, quarter: 1, eighth: 0.5, sixteenth: 0.25,
};

function pitchToFreq(pitch) {
  const match = pitch.match(/^([A-G])(#|b)?(\d)$/);
  if (!match) return 440;
  const [, name, accidental, octStr] = match;
  const key = accidental === '#' ? name + '#' : accidental === 'b' ? name + 'b' : name;
  const midi = NOTE_MIDI[key] + (parseInt(octStr) + 1) * 12;
  return 440 * Math.pow(2, (midi - 69) / 12);
}

function noteDuration(duration, dot, bpm) {
  const quarterSec = 60 / bpm;
  let beats = DURATION_BEATS[duration] || 1;
  if (dot) beats *= 1.5;
  return beats * quarterSec;
}

export default class AudioEngine {
  constructor() {
    this._ctx = null;
    this._stopFlag = false;
    this._playing = false;
  }

  _ensureCtx() {
    if (!this._ctx) this._ctx = new AudioContext();
    if (this._ctx.state === 'suspended') this._ctx.resume();
    return this._ctx;
  }

  get playing() { return this._playing; }

  _playTone(freq, duration) {
    const ctx = this._ensureCtx();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.value = freq;
    gain.gain.setValueAtTime(0, ctx.currentTime);
    gain.gain.linearRampToValueAtTime(0.3, ctx.currentTime + 0.02);
    gain.gain.setValueAtTime(0.3, ctx.currentTime + duration - 0.03);
    gain.gain.linearRampToValueAtTime(0, ctx.currentTime + duration);
    osc.connect(gain).connect(ctx.destination);
    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + duration);
  }

  async playSequence(notes, bpm, { speed = 1, onNote, onDone, startMeasure, endMeasure } = {}) {
    this._stopFlag = false;
    this._playing = true;
    const effectiveBpm = bpm * speed;

    let filtered = notes;
    if (startMeasure != null && endMeasure != null) {
      filtered = notes.filter(n => n.measure >= startMeasure && n.measure <= endMeasure);
    }
    const sorted = [...filtered].sort((a, b) => a.measure - b.measure || a.position - b.position);

    for (let i = 0; i < sorted.length; i++) {
      if (this._stopFlag) break;
      const note = sorted[i];
      const freq = pitchToFreq(note.pitch);
      const dur = noteDuration(note.duration, note.dot, effectiveBpm);
      if (onNote) onNote(note, i);
      this._playTone(freq, dur);
      await new Promise(r => setTimeout(r, dur * 1000 + 20));
    }
    this._playing = false;
    if (onDone && !this._stopFlag) onDone();
  }

  stop() {
    this._stopFlag = true;
    this._playing = false;
  }

  destroy() {
    this.stop();
    if (this._ctx) { this._ctx.close(); this._ctx = null; }
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/AudioEngine.js
git commit -m "feat: add Web Audio API engine for jianpu playback"
```

---

## Task 3: 前端 — PlayBar 播放控制栏组件

**Files:**
- Create: `frontend/src/PlayBar.jsx`

- [ ] **Step 1: 创建 PlayBar.jsx**

```jsx
import { useState, useCallback } from 'react';

const SPEEDS = [0.5, 0.75, 1, 1.25, 1.5];

export default function PlayBar({ engine, notes, bpm, onNoteHighlight, startMeasure, endMeasure, loop }) {
  const [playing, setPlaying] = useState(false);
  const [speed, setSpeed] = useState(1);
  const [currentIdx, setCurrentIdx] = useState(-1);

  const totalMeasures = notes.length > 0
    ? Math.max(...notes.map(n => n.measure))
    : 0;

  const currentMeasure = currentIdx >= 0 && notes[currentIdx]
    ? notes[currentIdx].measure
    : 0;

  const handlePlay = useCallback(async () => {
    if (!engine || playing) return;
    setPlaying(true);
    const play = async () => {
      await engine.playSequence(notes, bpm, {
        speed,
        startMeasure,
        endMeasure,
        onNote: (note, idx) => {
          setCurrentIdx(idx);
          if (onNoteHighlight) onNoteHighlight(note, idx);
        },
        onDone: () => {
          if (loop && !engine._stopFlag) {
            play();
          } else {
            setPlaying(false);
            setCurrentIdx(-1);
            if (onNoteHighlight) onNoteHighlight(null, -1);
          }
        },
      });
    };
    await play();
  }, [engine, notes, bpm, speed, playing, onNoteHighlight, startMeasure, endMeasure, loop]);

  const handleStop = useCallback(() => {
    if (engine) engine.stop();
    setPlaying(false);
    setCurrentIdx(-1);
    if (onNoteHighlight) onNoteHighlight(null, -1);
  }, [engine, onNoteHighlight]);

  const cycleSpeed = useCallback(() => {
    setSpeed(prev => {
      const idx = SPEEDS.indexOf(prev);
      return SPEEDS[(idx + 1) % SPEEDS.length];
    });
  }, []);

  return (
    <div className="play-bar">
      <button className="play-btn" onClick={playing ? handleStop : handlePlay}>
        {playing ? '⏹' : '▶'}
      </button>
      <div className="play-progress">
        <span>{currentMeasure} / {totalMeasures}</span>
      </div>
      <button className="speed-btn" onClick={cycleSpeed}>
        {speed}x
      </button>
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/PlayBar.jsx
git commit -m "feat: add PlayBar component for playback controls"
```

---

## Task 4: 前端 — DifficultyBadge 组件

**Files:**
- Create: `frontend/src/DifficultyBadge.jsx`

- [ ] **Step 1: 创建 DifficultyBadge.jsx**

```jsx
const LEVELS = {
  1: { label: '入门', color: '#52c41a', bg: '#f6ffed' },
  2: { label: '初级', color: '#1677ff', bg: '#e6f4ff' },
  3: { label: '中级', color: '#fa8c16', bg: '#fff7e6' },
};

export default function DifficultyBadge({ difficulty = 1 }) {
  const level = LEVELS[difficulty] || LEVELS[1];
  return (
    <span
      className="difficulty-badge"
      style={{ color: level.color, background: level.bg }}
    >
      {level.label}
    </span>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/DifficultyBadge.jsx
git commit -m "feat: add DifficultyBadge component"
```

---

## Task 5: 前端 — API 层更新

**Files:**
- Modify: `frontend/src/api.js`

- [ ] **Step 1: 修改 api.js — 添加 difficulty 筛选参数**

替换 `searchSongs` 函数：

```js
export const searchSongs = (q = '', page = 1, difficulty = null) =>
  api.get('/songs', { params: { q, page, ...(difficulty ? { difficulty } : {}) } }).then(r => r.data);
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/api.js
git commit -m "feat: add difficulty filter to searchSongs API"
```

---

## Task 6: 前端 — CSS 全面重写（白净风格）

**Files:**
- Modify: `frontend/src/index.css`

- [ ] **Step 1: 重写 index.css**

完整替换为白净风格。关键设计 token：

```css
:root {
  --primary: #4A90D9;
  --bg: #f8f9fa;
  --surface: #fff;
  --text: #1a1a1a;
  --text-secondary: #888;
  --border: #eee;
  --blow-color: #e74c3c;
  --draw-color: #2980b9;
  --shadow-card: 0 2px 8px rgba(0,0,0,0.04);
  --shadow-hover: 0 4px 16px rgba(0,0,0,0.08);
  --radius-card: 14px;
  --radius-btn: 10px;
  --radius-input: 12px;
  --diff-beginner: #52c41a;
  --diff-elementary: #1677ff;
  --diff-intermediate: #fa8c16;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg);
  color: var(--text);
  -webkit-font-smoothing: antialiased;
}

.app {
  max-width: 480px;
  margin: 0 auto;
  min-height: 100vh;
  background: var(--surface);
}

/* Header — 白底品牌色 */
.header {
  padding: 20px 16px 12px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
}

.header h1 {
  font-size: 22px;
  font-weight: 700;
  color: var(--primary);
}

.header p {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 2px;
}

/* Search */
.search-bar {
  padding: 12px 16px;
  position: sticky;
  top: 0;
  z-index: 10;
  background: var(--surface);
}

/* Filter bar */
.filter-bar {
  display: flex;
  gap: 8px;
  padding: 8px 16px;
  border-bottom: 1px solid var(--border);
  overflow-x: auto;
}

.filter-tag {
  padding: 4px 14px;
  border-radius: 16px;
  font-size: 13px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-secondary);
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}

.filter-tag.active {
  background: var(--primary);
  color: #fff;
  border-color: var(--primary);
}

/* Tab bar */
.tab-bar {
  display: flex;
  padding: 0 16px;
  border-bottom: 1px solid var(--border);
}

.tab-item {
  flex: 1;
  padding: 10px 0;
  text-align: center;
  font-size: 14px;
  color: var(--text-secondary);
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-item.active {
  color: var(--primary);
  border-bottom-color: var(--primary);
  font-weight: 500;
}

.fav-count {
  display: inline-block;
  background: var(--primary);
  color: #fff;
  font-size: 10px;
  padding: 0 5px;
  border-radius: 8px;
  margin-left: 4px;
  line-height: 16px;
}

/* Song cards */
.song-list { padding: 8px 16px; }

.song-card {
  padding: 14px 16px;
  margin-bottom: 10px;
  background: var(--surface);
  border-radius: var(--radius-card);
  box-shadow: var(--shadow-card);
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s;
  display: flex;
  align-items: center;
  border: 1px solid #f0f0f0;
}

.song-card:active {
  transform: translateY(-1px);
  box-shadow: var(--shadow-hover);
}

.song-card-main { flex: 1; min-width: 0; }

.song-card .title { font-size: 16px; font-weight: 500; }

.song-card .meta {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Difficulty badge */
.difficulty-badge {
  display: inline-block;
  font-size: 11px;
  padding: 1px 8px;
  border-radius: 10px;
  font-weight: 500;
}

/* Favorite buttons */
.fav-btn-sm {
  font-size: 18px;
  color: #ddd;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  flex-shrink: 0;
  transition: color 0.2s;
}

.fav-btn-sm.active { color: #faad14; }

/* Sheet view */
.sheet-header {
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid var(--border);
  background: var(--surface);
}

.sheet-header .back {
  font-size: 20px;
  cursor: pointer;
  padding: 4px;
  color: var(--primary);
}

.sheet-info { flex: 1; }
.sheet-info h2 { font-size: 18px; font-weight: 600; }
.sheet-info .meta { font-size: 12px; color: var(--text-secondary); }

.controls {
  padding: 8px 16px;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  border-bottom: 1px solid var(--border);
}

/* Sheet scroll area */
.sheet-scroll-area {
  overflow: auto;
  -webkit-overflow-scrolling: touch;
  padding: 16px 8px 80px;
  touch-action: pan-x pan-y pinch-zoom;
}

.sheet-canvas-wrap { padding: 0; }

.measure-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0;
}

.measure {
  display: inline-flex;
  align-items: flex-start;
  padding: 10px 4px;
  border-right: 2px solid #ccc;
  min-width: 0;
}

.measure:last-child { border-right: 3px double #999; }

.measure.selected { background: rgba(74, 144, 217, 0.06); }

.note-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 32px;
  padding: 0 3px;
  transition: transform 0.15s, background 0.15s;
  border-radius: 6px;
}

.note-col.highlight {
  background: rgba(74, 144, 217, 0.12);
  transform: scale(1.1);
}

.jianpu-num {
  font-size: 24px;
  font-weight: 700;
  line-height: 1.2;
  position: relative;
}

.jianpu-num.sharp::before {
  content: '#';
  font-size: 12px;
  position: absolute;
  left: -8px;
  top: -2px;
}

.octave-dot { font-size: 8px; line-height: 1; letter-spacing: 2px; }
.octave-dot.above { margin-bottom: -2px; }
.octave-dot.below { margin-top: -2px; }

.duration-line {
  width: 80%;
  height: 1.5px;
  background: #333;
  margin-top: 1px;
}

.hole-tag {
  margin-top: 6px;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 6px;
  line-height: 1.2;
}

.hole-tag.blow { color: var(--blow-color); background: rgba(231, 76, 60, 0.08); }
.hole-tag.draw { color: var(--draw-color); background: rgba(41, 128, 185, 0.08); }

.legend {
  padding: 8px 16px;
  font-size: 11px;
  color: var(--text-secondary);
  display: flex;
  gap: 16px;
  border-top: 1px solid var(--border);
}

.legend-item { display: flex; align-items: center; gap: 4px; }
.legend-dot { width: 8px; height: 8px; border-radius: 50%; }

/* Play bar */
.play-bar {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 480px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  background: var(--surface);
  border-top: 1px solid var(--border);
  box-shadow: 0 -2px 8px rgba(0,0,0,0.04);
  z-index: 20;
}

.play-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: var(--primary);
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.play-progress {
  flex: 1;
  font-size: 13px;
  color: var(--text-secondary);
}

.speed-btn {
  padding: 4px 12px;
  border-radius: var(--radius-btn);
  border: 1px solid var(--border);
  background: var(--surface);
  font-size: 13px;
  cursor: pointer;
  color: var(--text);
}

/* Empty & loading */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary);
}

.empty-state .icon { font-size: 48px; margin-bottom: 12px; }

.loading {
  text-align: center;
  padding: 40px;
  color: var(--text-secondary);
}

/* Zoom controls */
.zoom-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 6px 16px;
  border-bottom: 1px solid var(--border);
  font-size: 12px;
  color: var(--text-secondary);
}

.zoom-controls button {
  width: 28px;
  height: 28px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--surface);
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/index.css
git commit -m "feat: rewrite CSS to clean white style"
```

---

## Task 7: 前端 — App.jsx 重写（难度筛选 + 播放集成）

**Files:**
- Modify: `frontend/src/App.jsx`
- Modify: `frontend/src/JianpuRenderer.jsx`

- [ ] **Step 1: 重写 App.jsx**

关键变更：
1. 引入 `AudioEngine`、`PlayBar`、`DifficultyBadge`
2. 添加 `difficulty` 筛选状态和 filter-bar
3. 简谱页面集成 PlayBar
4. 传递 `highlightNote` 给 JianpuRenderer

```jsx
import { useState, useEffect, useCallback, useRef } from 'react';
import { SearchBar, Tag, Selector } from 'antd-mobile';
import { searchSongs, getHotSongs, getSong, getMapping, batchSongs } from './api';
import JianpuRenderer from './JianpuRenderer';
import PlayBar from './PlayBar';
import DifficultyBadge from './DifficultyBadge';
import AudioEngine from './AudioEngine';
import './index.css';

const KEYS = ['C', 'D', 'E', 'F', 'G', 'A', 'Bb'];
const TUNINGS = [
  { label: 'Paddy Richter', value: 'paddy' },
  { label: '标准 Richter', value: 'standard' },
];
const DIFF_FILTERS = [
  { label: '全部', value: null },
  { label: '入门', value: 1 },
  { label: '初级', value: 2 },
  { label: '中级', value: 3 },
];

function getFavIds() {
  try { return JSON.parse(localStorage.getItem('fav_ids') || '[]'); } catch { return []; }
}
function setFavIds(ids) { localStorage.setItem('fav_ids', JSON.stringify(ids)); }
function toggleFav(id) {
  const ids = getFavIds();
  const next = ids.includes(id) ? ids.filter(i => i !== id) : [...ids, id];
  setFavIds(next);
  return next;
}

export default function App() {
  const [view, setView] = useState('list');
  const [songs, setSongs] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [tab, setTab] = useState('all');
  const [favIds, setFavIdsState] = useState(getFavIds);
  const [diffFilter, setDiffFilter] = useState(null);

  const [currentSong, setCurrentSong] = useState(null);
  const [hKey, setHKey] = useState('C');
  const [tuning, setTuning] = useState('paddy');
  const [mapping, setMapping] = useState([]);
  const [zoom, setZoom] = useState(1);
  const [highlightNote, setHighlightNote] = useState(null);

  const engineRef = useRef(null);

  useEffect(() => {
    engineRef.current = new AudioEngine();
    return () => { if (engineRef.current) engineRef.current.destroy(); };
  }, []);

  useEffect(() => {
    getHotSongs().then(setSongs).catch(() => {});
  }, []);

  const handleSearch = useCallback((val) => {
    setQuery(val);
    setTab('all');
    if (!val.trim() && diffFilter == null) {
      getHotSongs().then(setSongs);
      return;
    }
    setLoading(true);
    searchSongs(val, 1, diffFilter).then(setSongs).finally(() => setLoading(false));
  }, [diffFilter]);

  const handleDiffFilter = useCallback((val) => {
    setDiffFilter(val);
    setTab('all');
    setLoading(true);
    searchSongs(query, 1, val).then(setSongs).finally(() => setLoading(false));
  }, [query]);

  const openSong = useCallback(async (id) => {
    setLoading(true);
    try {
      const [song, map] = await Promise.all([getSong(id), getMapping(hKey, tuning)]);
      setCurrentSong(song);
      setMapping(map.holes);
      setView('sheet');
      setZoom(1);
      setHighlightNote(null);
    } finally { setLoading(false); }
  }, [hKey, tuning]);

  useEffect(() => {
    if (view !== 'sheet') return;
    getMapping(hKey, tuning).then(r => setMapping(r.holes));
  }, [hKey, tuning, view]);

  const goBack = useCallback(() => {
    if (engineRef.current) engineRef.current.stop();
    setHighlightNote(null);
    setView('list');
  }, []);

  const handleToggleFav = useCallback((id) => {
    const next = toggleFav(id);
    setFavIdsState(next);
  }, []);

  const showFavorites = useCallback(() => {
    setTab('fav');
    const ids = getFavIds();
    if (ids.length === 0) { setSongs([]); return; }
    setLoading(true);
    batchSongs(ids).then(setSongs).finally(() => setLoading(false));
  }, []);

  const showAll = useCallback(() => {
    setTab('all');
    if (query) { searchSongs(query, 1, diffFilter).then(setSongs); }
    else { getHotSongs().then(setSongs); }
  }, [query, diffFilter]);

  const handleNoteHighlight = useCallback((note) => {
    setHighlightNote(note);
  }, []);

  // Sheet view
  if (view === 'sheet' && currentSong) {
    return (
      <div className="app">
        <div className="sheet-header">
          <span className="back" onClick={goBack}>←</span>
          <div className="sheet-info">
            <h2>{currentSong.title}</h2>
            <div className="meta">
              {currentSong.artist && <span>{currentSong.artist}</span>}
              <span>{currentSong.key}调</span>
              <span>{currentSong.time_signature}</span>
              <DifficultyBadge difficulty={currentSong.difficulty} />
            </div>
          </div>
          <button
            className={`fav-btn-sm${favIds.includes(currentSong.id) ? ' active' : ''}`}
            onClick={() => handleToggleFav(currentSong.id)}
          >
            {favIds.includes(currentSong.id) ? '★' : '☆'}
          </button>
        </div>

        <div className="controls">
          <Tag color={hKey === 'C' ? 'primary' : 'default'}>
            调性:
          </Tag>
          {KEYS.map(k => (
            <Tag key={k} color={hKey === k ? 'primary' : 'default'}
              onClick={() => setHKey(k)} style={{ cursor: 'pointer' }}>{k}</Tag>
          ))}
        </div>

        <div className="zoom-controls">
          <button onClick={() => setZoom(z => Math.max(0.5, z - 0.1))}>−</button>
          <span>{Math.round(zoom * 100)}%</span>
          <button onClick={() => setZoom(z => Math.min(2, z + 0.1))}>+</button>
        </div>

        <div className="sheet-scroll-area">
          <div style={{ transform: `scale(${zoom})`, transformOrigin: 'top left' }}>
            <JianpuRenderer
              notes={currentSong.notes || []}
              mapping={mapping}
              timeSignature={currentSong.time_signature}
              highlightNote={highlightNote}
            />
          </div>
        </div>

        <PlayBar
          engine={engineRef.current}
          notes={currentSong.notes || []}
          bpm={currentSong.bpm || 120}
          onNoteHighlight={handleNoteHighlight}
        />
      </div>
    );
  }

  // List view
  return (
    <div className="app">
      <div className="header">
        <h1>🎵 口琴简谱</h1>
        <p>Paddy Richter · 10孔布鲁斯口琴</p>
      </div>

      <div className="search-bar">
        <SearchBar placeholder="搜索歌曲或歌手" value={query} onChange={handleSearch} />
      </div>

      <div className="filter-bar">
        {DIFF_FILTERS.map(f => (
          <button
            key={String(f.value)}
            className={`filter-tag${diffFilter === f.value ? ' active' : ''}`}
            onClick={() => handleDiffFilter(f.value)}
          >
            {f.label}
          </button>
        ))}
      </div>

      <div className="tab-bar">
        <button className={`tab-item${tab === 'all' ? ' active' : ''}`} onClick={showAll}>全部</button>
        <button className={`tab-item${tab === 'fav' ? ' active' : ''}`} onClick={showFavorites}>
          ★ 收藏 {favIds.length > 0 && <span className="fav-count">{favIds.length}</span>}
        </button>
      </div>

      {loading && <div className="loading">加载中...</div>}

      <div className="song-list">
        {!loading && songs.length === 0 && (
          <div className="empty-state">
            <div className="icon">{tab === 'fav' ? '⭐' : '🎶'}</div>
            <p>{tab === 'fav' ? '还没有收藏歌曲' : query ? '没有找到相关歌曲' : '暂无歌曲'}</p>
          </div>
        )}
        {songs.map(song => (
          <div className="song-card" key={song.id} onClick={() => openSong(song.id)}>
            <div className="song-card-main">
              <div className="title">{song.title}</div>
              <div className="meta">
                {song.artist && <span>{song.artist}</span>}
                <span>{song.key}调</span>
                <DifficultyBadge difficulty={song.difficulty} />
              </div>
            </div>
            <button
              className={`fav-btn-sm${favIds.includes(song.id) ? ' active' : ''}`}
              onClick={(e) => { e.stopPropagation(); handleToggleFav(song.id); }}
            >
              {favIds.includes(song.id) ? '★' : '☆'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
```

- [ ] **Step 2: 修改 JianpuRenderer.jsx — 添加高亮支持**

在 `NoteColumn` 组件中添加 `highlightNote` prop 比较：

```jsx
// JianpuRenderer 新增 prop: highlightNote
export default function JianpuRenderer({ notes = [], mapping = [], timeSignature = '4/4', highlightNote = null }) {
  // ... holeLookup 和 measures 不变 ...

  return (
    <div className="sheet-canvas-wrap">
      <div className="measure-row">
        {measures.map((measureNotes, mi) => (
          <div className="measure" key={mi}>
            {measureNotes.map((note, ni) => (
              <NoteColumn
                key={ni}
                note={note}
                holeLookup={holeLookup}
                isHighlighted={highlightNote && highlightNote.measure === note.measure && highlightNote.position === note.position}
              />
            ))}
          </div>
        ))}
      </div>
      <div className="legend">
        <div className="legend-item">
          <div className="legend-dot" style={{ background: 'var(--blow-color)' }} />
          <span>吹 ↑</span>
        </div>
        <div className="legend-item">
          <div className="legend-dot" style={{ background: 'var(--draw-color)' }} />
          <span>吸 ↓</span>
        </div>
      </div>
    </div>
  );
}

// NoteColumn 新增 isHighlighted prop
function NoteColumn({ note, holeLookup, isHighlighted = false }) {
  const jp = pitchToJianpu(note.pitch);
  const holeInfo = holeLookup[note.pitch];
  const lines = durationLines(note.duration);

  return (
    <div className={`note-col${isHighlighted ? ' highlight' : ''}`}>
      {jp.octaveDots > 0 && (
        <div className="octave-dot above">{'·'.repeat(jp.octaveDots)}</div>
      )}
      <div className={`jianpu-num${jp.sharp ? ' sharp' : ''}`}>
        {jp.flat && <span style={{ fontSize: 12, position: 'absolute', left: -8, top: -2 }}>♭</span>}
        {jp.num}
        {note.dot ? '·' : ''}
      </div>
      {jp.octaveDots < 0 && (
        <div className="octave-dot below">{'·'.repeat(Math.abs(jp.octaveDots))}</div>
      )}
      {Array.from({ length: lines }).map((_, i) => (
        <div className="duration-line" key={i} />
      ))}
      {holeInfo ? (
        <div className={`hole-tag ${holeInfo.action}`}>
          {holeInfo.hole}{holeInfo.action === 'blow' ? '↑' : '↓'}
        </div>
      ) : (
        <div className="hole-tag" style={{ opacity: 0.3 }}>-</div>
      )}
    </div>
  );
}
```

- [ ] **Step 3: 验证前端编译无报错**

Run: `cd frontend && npx vite build`
Expected: 编译成功

- [ ] **Step 4: Commit**

```bash
git add frontend/src/App.jsx frontend/src/JianpuRenderer.jsx
git commit -m "feat: integrate playback, difficulty filter, and new UI"
```

---

## Task 8: 后端 — 爬取器重写 (jianpu.cn)

**Files:**
- Modify: `backend/app/pipeline/scraper.py`
- Modify: `backend/app/pipeline/parser.py`

- [ ] **Step 1: 重写 scraper.py**

jianpu.cn 的简谱是图片格式，无法直接解析为音符数据。爬取器的职责是：搜索 → 抓取详情页 → 提取元信息（标题、歌手）+ 简谱图片 URL。后续可通过 LLM Vision 或 OCR 提取音符。

```python
"""Web scraper for jianpu.cn — extracts song metadata and jianpu image URLs."""
import asyncio
import logging
import re

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}
REQUEST_DELAY = 2.0
BASE_URL = "http://www.jianpu.cn"


async def scrape_jianpu(params: dict) -> dict:
    """Task handler: scrape jianpu.cn for song listings."""
    query = params.get("query", "")
    max_results = min(params.get("max_results", 10), 20)

    if not query.strip():
        return {"error": "搜索关键词不能为空", "songs": [], "count": 0}

    try:
        results = await _search_and_fetch(query, max_results)
        return {
            "message": f"从 jianpu.cn 搜索到 {len(results)} 首（简谱为图片，需 OCR/LLM 提取音符）",
            "songs": results,
            "count": len(results),
        }
    except Exception as e:
        logger.exception("Scrape failed")
        return {"error": str(e), "songs": [], "count": 0}


async def _search_and_fetch(query: str, max_results: int) -> list[dict]:
    results = []
    async with httpx.AsyncClient(timeout=15, headers=HEADERS, follow_redirects=True) as client:
        # Step 1: search
        try:
            resp = await client.get(f"{BASE_URL}/so.htm", params={"q": query})
            resp.raise_for_status()
        except httpx.HTTPError as e:
            logger.error("Search request failed: %s", e)
            return []

        soup = BeautifulSoup(resp.content, "lxml")
        links = _extract_search_links(soup, max_results)

        # Step 2: fetch each detail page
        for item in links:
            await asyncio.sleep(REQUEST_DELAY)
            try:
                detail = await _fetch_detail(client, item["url"])
                results.append({**item, **detail})
            except Exception as e:
                logger.warning("Detail fetch failed for %s: %s", item["url"], e)
                results.append({**item, "images": [], "error": str(e)})

    return results


def _extract_search_links(soup: BeautifulSoup, max_results: int) -> list[dict]:
    links = []
    for a in soup.find_all("a", href=re.compile(r"/pu/\d+/\d+\.htm")):
        title = a.get_text(strip=True)
        href = a.get("href", "")
        if not title or not href:
            continue
        url = href if href.startswith("http") else BASE_URL + href
        links.append({"title": title, "url": url})
        if len(links) >= max_results:
            break
    return links


async def _fetch_detail(client: httpx.AsyncClient, url: str) -> dict:
    resp = await client.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "lxml")

    images = []
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if not src:
            continue
        if any(ext in src.lower() for ext in (".jpg", ".png", ".gif")):
            if not src.startswith("http"):
                src = BASE_URL + "/" + src.lstrip("/")
            images.append(src)

    # Try to extract artist from page title or meta
    artist = ""
    page_title = soup.find("title")
    if page_title:
        text = page_title.get_text()
        # Common pattern: "歌名 - 歌手 简谱"
        m = re.search(r"[-–—]\s*(.+?)\s*简谱", text)
        if m:
            artist = m.group(1).strip()

    return {"images": images[:5], "artist": artist}
```

- [ ] **Step 2: 重写 parser.py**

简化为只保留 jianpu.cn 解析器，移除未实现的占位类：

```python
"""Jianpu page parser for jianpu.cn."""
import logging
import re

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def parse_search_results(html: str, base_url: str = "http://www.jianpu.cn") -> list[dict]:
    """Parse jianpu.cn search results page. Returns list of {title, url}."""
    soup = BeautifulSoup(html, "lxml")
    results = []
    for a in soup.find_all("a", href=re.compile(r"/pu/\d+/\d+\.htm")):
        title = a.get_text(strip=True)
        href = a.get("href", "")
        if title and href:
            url = href if href.startswith("http") else base_url + href
            results.append({"title": title, "url": url})
    return results


def parse_detail_page(html: str, base_url: str = "http://www.jianpu.cn") -> dict:
    """Parse jianpu.cn detail page. Returns {title, artist, images}."""
    soup = BeautifulSoup(html, "lxml")

    title = ""
    artist = ""
    page_title = soup.find("title")
    if page_title:
        text = page_title.get_text()
        # Pattern: "歌名 - 歌手 简谱"
        m = re.match(r"(.+?)\s*[-–—]\s*(.+?)\s*简谱", text)
        if m:
            title = m.group(1).strip()
            artist = m.group(2).strip()
        else:
            title = text.replace("简谱", "").strip()

    images = []
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src and any(ext in src.lower() for ext in (".jpg", ".png", ".gif")):
            if not src.startswith("http"):
                src = base_url + "/" + src.lstrip("/")
            images.append(src)

    return {"title": title, "artist": artist, "images": images[:5]}
```

- [ ] **Step 3: Commit**

```bash
git add backend/app/pipeline/scraper.py backend/app/pipeline/parser.py
git commit -m "feat: rewrite scraper and parser for jianpu.cn"
```

---

## Task 9: 后端 — 曲库扩充 (30+ 首 seed data)

**Files:**
- Create: `backend/app/seed_songs.py`
- Modify: `backend/app/main.py`

- [ ] **Step 1: 创建 seed_songs.py**

将现有 `_get_seed_data()` 从 main.py 提取到独立文件，并扩充至 30+ 首。每首歌增加 `difficulty` 字段。

文件结构：

```python
"""Seed song data for harmonica-tab. 30+ songs with jianpu note sequences."""


def get_seed_data():
    """Return all seed songs. Each note tuple: (measure, position, pitch, duration, dot?, tie?)"""
    return [
        *_children_songs(),
        *_pop_songs(),
        *_folk_songs(),
        *_foreign_classics(),
    ]


def _children_songs():
    return [
        {
            "title": "小星星", "artist": "儿歌", "key": "C", "ts": "4/4", "bpm": 100, "difficulty": 1,
            "notes": [
                (1,1,"C4","quarter"), (1,2,"C4","quarter"), (1,3,"G4","quarter"), (1,4,"G4","quarter"),
                (2,1,"A4","quarter"), (2,2,"A4","quarter"), (2,3,"G4","half"),
                (3,1,"F4","quarter"), (3,2,"F4","quarter"), (3,3,"E4","quarter"), (3,4,"E4","quarter"),
                (4,1,"D4","quarter"), (4,2,"D4","quarter"), (4,3,"C4","half"),
                (5,1,"G4","quarter"), (5,2,"G4","quarter"), (5,3,"F4","quarter"), (5,4,"F4","quarter"),
                (6,1,"E4","quarter"), (6,2,"E4","quarter"), (6,3,"D4","half"),
                (7,1,"G4","quarter"), (7,2,"G4","quarter"), (7,3,"F4","quarter"), (7,4,"F4","quarter"),
                (8,1,"E4","quarter"), (8,2,"E4","quarter"), (8,3,"D4","half"),
            ],
        },
        # ... 保留现有 8 首 + 新增儿歌 ...
        {
            "title": "找朋友", "artist": "儿歌", "key": "C", "ts": "2/4", "bpm": 108, "difficulty": 1,
            "notes": [
                (1,1,"C4","eighth"), (1,2,"C4","eighth"), (1,3,"E4","eighth"), (1,4,"E4","eighth"),
                (2,1,"G4","quarter"), (2,2,"E4","quarter"),
                (3,1,"F4","eighth"), (3,2,"F4","eighth"), (3,3,"E4","eighth"), (3,4,"D4","eighth"),
                (4,1,"C4","half"),
            ],
        },
        {
            "title": "粉刷匠", "artist": "儿歌", "key": "C", "ts": "2/4", "bpm": 112, "difficulty": 1,
            "notes": [
                (1,1,"E4","eighth"), (1,2,"E4","eighth"), (1,3,"F4","eighth"), (1,4,"G4","eighth"),
                (2,1,"G4","eighth"), (2,2,"G4","eighth"), (2,3,"G4","quarter"),
                (3,1,"A4","eighth"), (3,2,"G4","eighth"), (3,3,"F4","eighth"), (3,4,"E4","eighth"),
                (4,1,"D4","half"),
                (5,1,"C4","eighth"), (5,2,"C4","eighth"), (5,3,"D4","eighth"), (5,4,"E4","eighth"),
                (6,1,"E4","eighth"), (6,2,"D4","eighth"), (6,3,"D4","quarter"),
                (7,1,"C4","eighth"), (7,2,"C4","eighth"), (7,3,"D4","eighth"), (7,4,"E4","eighth"),
                (8,1,"D4","eighth"), (8,2,"C4","eighth"), (8,3,"C4","quarter"),
            ],
        },
        # ... 小毛驴、数鸭子、拔萝卜 ...
    ]


def _pop_songs():
    """流行金曲 — 10 首"""
    return [
        {
            "title": "甜蜜蜜", "artist": "邓丽君", "key": "C", "ts": "4/4", "bpm": 108, "difficulty": 2,
            "notes": [
                (1,1,"E4","quarter"), (1,2,"E4","eighth"), (1,3,"D4","eighth"), (1,4,"E4","quarter"), (1,5,"G4","quarter"),
                (2,1,"A4","quarter"), (2,2,"G4","quarter"), (2,3,"E4","half"),
                (3,1,"D4","quarter"), (3,2,"E4","quarter"), (3,3,"G4","quarter"), (3,4,"E4","quarter"),
                (4,1,"D4","whole"),
            ],
        },
        # ... 其余 9 首流行歌 ...
    ]


def _folk_songs():
    """民歌/经典 — 5 首"""
    return [
        {
            "title": "茉莉花", "artist": "民歌", "key": "C", "ts": "2/4", "bpm": 80, "difficulty": 2,
            "notes": [
                (1,1,"E4","eighth"), (1,2,"E4","eighth"), (1,3,"E4","eighth"), (1,4,"F4","eighth"),
                (2,1,"G4","eighth"), (2,2,"A4","eighth"), (2,3,"G4","quarter"),
                (3,1,"E4","eighth"), (3,2,"E4","eighth"), (3,3,"D4","eighth"), (3,4,"E4","eighth"),
                (4,1,"G4","eighth"), (4,2,"E4","eighth"), (4,3,"D4","quarter"),
            ],
        },
        {
            "title": "送别", "artist": "李叔同", "key": "C", "ts": "4/4", "bpm": 72, "difficulty": 2,
            "notes": [
                (1,1,"E4","quarter",1), (1,2,"C4","eighth"), (1,3,"E4","quarter"), (1,4,"G4","quarter"),
                (2,1,"A4","half"), (2,2,"G4","half"),
                (3,1,"E4","quarter"), (3,2,"C5","quarter"), (3,3,"B4","quarter"), (3,4,"A4","quarter"),
                (4,1,"G4","whole"),
            ],
        },
        # ... 康定情歌、南泥湾、映山红 ...
    ]


def _foreign_classics():
    """外国经典 — 5 首"""
    return [
        {
            "title": "Amazing Grace", "artist": "John Newton", "key": "C", "ts": "3/4", "bpm": 80, "difficulty": 2,
            "notes": [
                (1,1,"C4","quarter"),
                (2,1,"E4","half"), (2,2,"E4","eighth"), (2,3,"D4","eighth"),
                (3,1,"E4","half"), (3,2,"G4","quarter"),
                (4,1,"G4","half"), (4,2,"E4","quarter"),
                (5,1,"E4","half"), (5,2,"E4","eighth"), (5,3,"D4","eighth"),
                (6,1,"C4","half"), (6,2,"C4","quarter"),
            ],
        },
        {
            "title": "Auld Lang Syne", "artist": "Robert Burns", "key": "C", "ts": "4/4", "bpm": 100, "difficulty": 1,
            "notes": [
                (1,1,"C4","quarter"),
                (2,1,"F4","quarter",1), (2,2,"F4","eighth"), (2,3,"F4","quarter"), (2,4,"A4","quarter"),
                (3,1,"G4","quarter",1), (3,2,"F4","eighth"), (3,3,"G4","quarter"), (3,4,"A4","quarter"),
                (4,1,"F4","quarter",1), (4,2,"F4","eighth"), (4,3,"A4","quarter"), (4,4,"C5","quarter"),
                (5,1,"D5","half",1),
            ],
        },
        # ... Edelweiss, Yesterday, My Heart Will Go On ...
    ]
```

注意：上面展示了文件结构和部分歌曲。实际实现时需要为每首歌编写完整的音符序列。这是最耗时的任务——每首歌需要手动转录简谱。建议分批完成：先补全儿歌和民歌（旋律简单），再做流行和外国经典。

- [ ] **Step 2: 修改 main.py — 引用 seed_songs.py**

替换 `_get_seed_data` 和 `_seed_songs`：

```python
# 在 main.py 顶部添加
from .seed_songs import get_seed_data

# 删除 _get_seed_data() 函数

# 修改 _seed_songs:
async def _seed_songs(db):
    """Insert demo songs with jianpu note data."""
    songs = get_seed_data()
    for song in songs:
        cursor = await db.execute(
            "INSERT INTO songs (title, artist, key, time_signature, bpm, source, verified, status, difficulty) VALUES (?,?,?,?,?,?,?,?,?)",
            (song["title"], song["artist"], song["key"], song["ts"], song["bpm"], "manual", 1, "verified", song.get("difficulty", 1)),
        )
        song_id = cursor.lastrowid
        for note in song["notes"]:
            await db.execute(
                "INSERT INTO notes (song_id, measure, position, pitch, duration, dot, tie) VALUES (?,?,?,?,?,?,?)",
                (song_id, note[0], note[1], note[2], note[3], note[4] if len(note) > 4 else 0, note[5] if len(note) > 5 else 0),
            )
```

- [ ] **Step 3: Commit**

```bash
git add backend/app/seed_songs.py backend/app/main.py
git commit -m "feat: expand song library to 30+ songs with difficulty levels"
```

---

## Task 10: 构建 + 部署

**Files:**
- Modify: `frontend/` (build)
- Server: `115.190.112.212`

- [ ] **Step 1: 前端构建**

```bash
cd frontend && npm run build
```

Expected: `dist/` 目录生成成功

- [ ] **Step 2: 删除服务器旧数据库（触发 seed 重新生成）**

```bash
ssh -i "E:\Workspace\claude\115.190.112.212 SSH Secret.pem" root@115.190.112.212 \
  "cd /var/www/harmonica-tab && rm -f backend/harmonica.db"
```

- [ ] **Step 3: 推送代码到 GitHub**

```bash
git add -A
git commit -m "feat: Phase 3 — UI upgrade, playback, difficulty, scraper, 30+ songs"
git push origin main
```

- [ ] **Step 4: 服务器拉取并重启**

```bash
ssh -i "E:\Workspace\claude\115.190.112.212 SSH Secret.pem" root@115.190.112.212 \
  "cd /var/www/harmonica-tab && git pull origin main && systemctl restart harmonica-tab"
```

- [ ] **Step 5: 验证部署**

访问 http://115.190.112.212:5123 确认：
- 新 UI 白净风格生效
- 难度筛选可用
- 30+ 首歌曲显示
- 播放功能正常
- 管理后台 /admin 正常
