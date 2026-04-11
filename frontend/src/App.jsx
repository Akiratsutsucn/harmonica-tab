import { useState, useEffect, useCallback } from 'react';
import { SearchBar, Tag, Selector } from 'antd-mobile';
import { searchSongs, getHotSongs, getSong, getMapping, batchSongs } from './api';
import JianpuRenderer from './JianpuRenderer';
import './index.css';

const KEYS = ['C', 'D', 'E', 'F', 'G', 'A', 'Bb'];
const TUNINGS = [
  { label: 'Paddy Richter', value: 'paddy' },
  { label: '标准 Richter', value: 'standard' },
];

// --- Favorites helpers (localStorage) ---
function getFavIds() {
  try { return JSON.parse(localStorage.getItem('fav_ids') || '[]'); } catch { return []; }
}
function setFavIds(ids) {
  localStorage.setItem('fav_ids', JSON.stringify(ids));
}
function toggleFav(id) {
  const ids = getFavIds();
  const next = ids.includes(id) ? ids.filter(i => i !== id) : [...ids, id];
  setFavIds(next);
  return next;
}

export default function App() {
  const [view, setView] = useState('list'); // 'list' | 'sheet'
  const [songs, setSongs] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [tab, setTab] = useState('all'); // 'all' | 'fav'
  const [favIds, setFavIdsState] = useState(getFavIds);

  // Sheet view state
  const [currentSong, setCurrentSong] = useState(null);
  const [hKey, setHKey] = useState('C');
  const [tuning, setTuning] = useState('paddy');
  const [mapping, setMapping] = useState([]);
  const [zoom, setZoom] = useState(1);

  // Load hot songs on mount
  useEffect(() => {
    getHotSongs().then(setSongs).catch(() => {});
  }, []);

  // Search
  const handleSearch = useCallback((val) => {
    setQuery(val);
    setTab('all');
    if (!val.trim()) {
      getHotSongs().then(setSongs);
      return;
    }
    setLoading(true);
    searchSongs(val).then(setSongs).finally(() => setLoading(false));
  }, []);

  // Open song
  const openSong = useCallback(async (id) => {
    setLoading(true);
    try {
      const [song, map] = await Promise.all([
        getSong(id),
        getMapping(hKey, tuning),
      ]);
      setCurrentSong(song);
      setMapping(map.holes);
      setView('sheet');
      setZoom(1);
    } finally {
      setLoading(false);
    }
  }, [hKey, tuning]);

  // Reload mapping when key/tuning changes
  useEffect(() => {
    if (view !== 'sheet') return;
    getMapping(hKey, tuning).then(r => setMapping(r.holes));
  }, [hKey, tuning, view]);

  const goBack = () => {
    setView('list');
    setCurrentSong(null);
  };

  // Toggle favorite
  const handleToggleFav = (id) => {
    const next = toggleFav(id);
    setFavIdsState(next);
  };

  // Show favorites tab
  const showFavorites = useCallback(async () => {
    setTab('fav');
    setQuery('');
    const ids = getFavIds();
    if (ids.length === 0) {
      setSongs([]);
      return;
    }
    setLoading(true);
    try {
      const data = await batchSongs(ids);
      setSongs(data);
    } finally {
      setLoading(false);
    }
  }, []);

  const showAll = useCallback(() => {
    setTab('all');
    setQuery('');
    getHotSongs().then(setSongs);
  }, []);

  // Sheet view
  if (view === 'sheet' && currentSong) {
    const isFav = favIds.includes(currentSong.id);
    return (
      <div className="app">
        <div className="sheet-header">
          <span className="back" onClick={goBack} role="button" tabIndex={0} onKeyDown={e => e.key === 'Enter' && goBack()}>←</span>
          <div className="sheet-info">
            <h2>{currentSong.title}</h2>
            <div className="meta">
              {currentSong.artist && <span>{currentSong.artist}</span>}
              <span>{currentSong.key}调</span>
              <span>{currentSong.time_signature}</span>
              <span>♩={currentSong.bpm}</span>
            </div>
          </div>
          <button
            className={`fav-btn${isFav ? ' active' : ''}`}
            onClick={() => handleToggleFav(currentSong.id)}
            aria-label={isFav ? '取消收藏' : '收藏'}
          >
            {isFav ? '★' : '☆'}
          </button>
        </div>

        <div className="controls">
          <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <span style={{ fontSize: 12, color: '#999' }}>口琴调:</span>
            {KEYS.map(k => (
              <Tag
                key={k}
                color={hKey === k ? 'primary' : 'default'}
                onClick={() => setHKey(k)}
                style={{ cursor: 'pointer' }}
              >
                {k}
              </Tag>
            ))}
          </div>
          <Selector
            options={TUNINGS}
            value={[tuning]}
            onChange={v => v.length && setTuning(v[0])}
            style={{ fontSize: 12 }}
          />
        </div>

        <div className="zoom-controls">
          <button onClick={() => setZoom(z => Math.max(0.6, z - 0.1))}>−</button>
          <span>{Math.round(zoom * 100)}%</span>
          <button onClick={() => setZoom(z => Math.min(1.6, z + 0.1))}>+</button>
          <button onClick={() => setZoom(1)}>重置</button>
        </div>

        <div className="sheet-scroll-area">
          <div style={{ transform: `scale(${zoom})`, transformOrigin: 'top left', minWidth: zoom < 1 ? `${100 / zoom}%` : 'auto' }}>
            <JianpuRenderer
              notes={currentSong.notes}
              mapping={mapping}
              timeSignature={currentSong.time_signature}
            />
          </div>
        </div>
      </div>
    );
  }

  // List view
  return (
    <div className="app">
      <div className="header">
        <h1>🎵 口琴简谱</h1>
        <p>搜索歌曲 · 查看简谱 · 对照孔位</p>
      </div>

      <div className="search-bar">
        <SearchBar
          placeholder="搜索歌名或歌手"
          value={query}
          onChange={handleSearch}
          onSearch={handleSearch}
        />
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
                <span>{song.time_signature}</span>
              </div>
            </div>
            <button
              className={`fav-btn-sm${favIds.includes(song.id) ? ' active' : ''}`}
              onClick={(e) => { e.stopPropagation(); handleToggleFav(song.id); }}
              aria-label={favIds.includes(song.id) ? '取消收藏' : '收藏'}
            >
              {favIds.includes(song.id) ? '★' : '☆'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
