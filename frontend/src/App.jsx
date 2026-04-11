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
          <Tag color={hKey === 'C' ? 'primary' : 'default'}>调性:</Tag>
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
