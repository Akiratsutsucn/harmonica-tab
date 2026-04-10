import { useState, useEffect, useCallback } from 'react';
import { SearchBar, Tag, Selector } from 'antd-mobile';
import { searchSongs, getHotSongs, getSong, getMapping } from './api';
import JianpuRenderer from './JianpuRenderer';
import './index.css';

const KEYS = ['C', 'D', 'E', 'F', 'G', 'A', 'Bb'];
const TUNINGS = [
  { label: 'Paddy Richter', value: 'paddy' },
  { label: '标准 Richter', value: 'standard' },
];

export default function App() {
  const [view, setView] = useState('list'); // 'list' | 'sheet'
  const [songs, setSongs] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);

  // Sheet view state
  const [currentSong, setCurrentSong] = useState(null);
  const [hKey, setHKey] = useState('C');
  const [tuning, setTuning] = useState('paddy');
  const [mapping, setMapping] = useState([]);

  // Load hot songs on mount
  useEffect(() => {
    getHotSongs().then(setSongs).catch(() => {});
  }, []);

  // Search
  const handleSearch = useCallback((val) => {
    setQuery(val);
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

  if (view === 'sheet' && currentSong) {
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

        <JianpuRenderer
          notes={currentSong.notes}
          mapping={mapping}
          timeSignature={currentSong.time_signature}
        />
      </div>
    );
  }

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

      {loading && <div className="loading">加载中...</div>}

      <div className="song-list">
        {!loading && songs.length === 0 && (
          <div className="empty-state">
            <div className="icon">🎶</div>
            <p>{query ? '没有找到相关歌曲' : '暂无歌曲'}</p>
          </div>
        )}
        {songs.map(song => (
          <div className="song-card" key={song.id} onClick={() => openSong(song.id)}>
            <div className="title">{song.title}</div>
            <div className="meta">
              {song.artist && <span>{song.artist}</span>}
              <span>{song.key}调</span>
              <span>{song.time_signature}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
