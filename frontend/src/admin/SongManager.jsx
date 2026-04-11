import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  getAdminSongs, createSong, updateSong, deleteSong,
  verifySong, rejectSong, submitAIGenerate,
} from '../adminApi';

const STATUS_MAP = {
  verified: { label: '已审核', color: '#52c41a' },
  pending: { label: '待审核', color: '#faad14' },
  rejected: { label: '已驳回', color: '#ff4d4f' },
};

export default function SongManager() {
  const navigate = useNavigate();
  const [songs, setSongs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState({ status: '', source: '', q: '' });
  const [showAdd, setShowAdd] = useState(false);
  const [showAI, setShowAI] = useState(false);
  const [editId, setEditId] = useState(null);

  const load = useCallback(() => {
    setLoading(true);
    const params = {};
    if (filter.status) params.status = filter.status;
    if (filter.source) params.source = filter.source;
    if (filter.q) params.q = filter.q;
    getAdminSongs(params).then(setSongs).finally(() => setLoading(false));
  }, [filter]);

  useEffect(() => { load(); }, [load]);

  const handleVerify = async (id) => {
    await verifySong(id);
    load();
  };

  const handleReject = async (id) => {
    await rejectSong(id);
    load();
  };

  const handleDelete = async (id) => {
    if (!confirm('确定删除？')) return;
    await deleteSong(id);
    load();
  };

  return (
    <div className="song-manager">
      <div className="manager-header">
        <h2>歌曲管理</h2>
        <div className="header-actions">
          <button className="btn btn-primary" onClick={() => setShowAdd(true)}>新增歌曲</button>
          <button className="btn btn-secondary" onClick={() => setShowAI(true)}>AI 生成</button>
        </div>
      </div>

      <div className="filters">
        <input
          placeholder="搜索歌名/歌手"
          value={filter.q}
          onChange={e => setFilter(f => ({ ...f, q: e.target.value }))}
        />
        <select value={filter.status} onChange={e => setFilter(f => ({ ...f, status: e.target.value }))}>
          <option value="">全部状态</option>
          <option value="verified">已审核</option>
          <option value="pending">待审核</option>
          <option value="rejected">已驳回</option>
        </select>
        <select value={filter.source} onChange={e => setFilter(f => ({ ...f, source: e.target.value }))}>
          <option value="">全部来源</option>
          <option value="manual">手动</option>
          <option value="ai">AI</option>
          <option value="crawl">爬取</option>
          <option value="import">导入</option>
        </select>
      </div>

      {loading ? (
        <div className="admin-loading">加载中...</div>
      ) : (
        <div className="song-table">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>歌名</th>
                <th>歌手</th>
                <th>调</th>
                <th>来源</th>
                <th>状态</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              {songs.map(s => (
                <tr key={s.id}>
                  <td>{s.id}</td>
                  <td>{s.title}</td>
                  <td>{s.artist}</td>
                  <td>{s.key}</td>
                  <td>{s.source}</td>
                  <td>
                    <span className="status-tag" style={{ color: STATUS_MAP[s.status]?.color }}>
                      {STATUS_MAP[s.status]?.label || s.status}
                    </span>
                  </td>
                  <td className="actions">
                    <button className="btn-sm" onClick={() => navigate(`/admin/songs/${s.id}/notes`)}>编辑谱</button>
                    <button className="btn-sm" onClick={() => setEditId(s.id)}>编辑</button>
                    {s.status !== 'verified' && (
                      <button className="btn-sm btn-success" onClick={() => handleVerify(s.id)}>通过</button>
                    )}
                    {s.status !== 'rejected' && (
                      <button className="btn-sm btn-warn" onClick={() => handleReject(s.id)}>驳回</button>
                    )}
                    <button className="btn-sm btn-danger" onClick={() => handleDelete(s.id)}>删除</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {songs.length === 0 && <div className="empty">暂无歌曲</div>}
        </div>
      )}

      {showAdd && <AddSongModal onClose={() => setShowAdd(false)} onDone={() => { setShowAdd(false); load(); }} />}
      {showAI && <AIGenerateModal onClose={() => setShowAI(false)} />}
      {editId && <EditSongModal id={editId} songs={songs} onClose={() => setEditId(null)} onDone={() => { setEditId(null); load(); }} />}
    </div>
  );
}

function AddSongModal({ onClose, onDone }) {
  const [form, setForm] = useState({ title: '', artist: '', key: 'C', time_signature: '4/4', bpm: 120 });

  const handleSubmit = async (e) => {
    e.preventDefault();
    await createSong({ ...form, status: 'pending', source: 'manual' });
    onDone();
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <h3>新增歌曲</h3>
        <form onSubmit={handleSubmit}>
          <label>歌名 <input required value={form.title} onChange={e => setForm(f => ({ ...f, title: e.target.value }))} /></label>
          <label>歌手 <input value={form.artist} onChange={e => setForm(f => ({ ...f, artist: e.target.value }))} /></label>
          <label>调 <input value={form.key} onChange={e => setForm(f => ({ ...f, key: e.target.value }))} /></label>
          <label>拍号 <input value={form.time_signature} onChange={e => setForm(f => ({ ...f, time_signature: e.target.value }))} /></label>
          <label>BPM <input type="number" value={form.bpm} onChange={e => setForm(f => ({ ...f, bpm: +e.target.value }))} /></label>
          <div className="modal-actions">
            <button type="button" onClick={onClose}>取消</button>
            <button type="submit" className="btn-primary">创建</button>
          </div>
        </form>
      </div>
    </div>
  );
}

function EditSongModal({ id, songs, onClose, onDone }) {
  const song = songs.find(s => s.id === id);
  const [form, setForm] = useState({
    title: song?.title || '',
    artist: song?.artist || '',
    key: song?.key || 'C',
    time_signature: song?.time_signature || '4/4',
    bpm: song?.bpm || 120,
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    await updateSong(id, form);
    onDone();
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <h3>编辑歌曲</h3>
        <form onSubmit={handleSubmit}>
          <label>歌名 <input required value={form.title} onChange={e => setForm(f => ({ ...f, title: e.target.value }))} /></label>
          <label>歌手 <input value={form.artist} onChange={e => setForm(f => ({ ...f, artist: e.target.value }))} /></label>
          <label>调 <input value={form.key} onChange={e => setForm(f => ({ ...f, key: e.target.value }))} /></label>
          <label>拍号 <input value={form.time_signature} onChange={e => setForm(f => ({ ...f, time_signature: e.target.value }))} /></label>
          <label>BPM <input type="number" value={form.bpm} onChange={e => setForm(f => ({ ...f, bpm: +e.target.value }))} /></label>
          <div className="modal-actions">
            <button type="button" onClick={onClose}>取消</button>
            <button type="submit" className="btn-primary">保存</button>
          </div>
        </form>
      </div>
    </div>
  );
}

function AIGenerateModal({ onClose }) {
  const [form, setForm] = useState({ title: '', artist: '', original_key: '', time_signature: '4/4' });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await submitAIGenerate(form);
    setSubmitted(true);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <h3>AI 生成简谱</h3>
        {submitted ? (
          <div className="success-msg">
            <p>任务已提交，请在任务监控中查看进度</p>
            <button onClick={onClose}>关闭</button>
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <label>歌名 <input required value={form.title} onChange={e => setForm(f => ({ ...f, title: e.target.value }))} /></label>
            <label>歌手 <input value={form.artist} onChange={e => setForm(f => ({ ...f, artist: e.target.value }))} /></label>
            <label>原调 <input placeholder="可选" value={form.original_key} onChange={e => setForm(f => ({ ...f, original_key: e.target.value }))} /></label>
            <label>拍号 <input value={form.time_signature} onChange={e => setForm(f => ({ ...f, time_signature: e.target.value }))} /></label>
            <div className="modal-actions">
              <button type="button" onClick={onClose}>取消</button>
              <button type="submit" className="btn-primary">提交生成</button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
