import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getSongNotes, updateSongNotes } from '../adminApi';
import { getSong, getMapping } from '../api';
import JianpuRenderer from '../JianpuRenderer';

const DURATIONS = ['whole', 'half', 'quarter', 'eighth', 'sixteenth'];
const PITCHES = ['C', 'D', 'E', 'F', 'G', 'A', 'B'];

export default function NoteEditor() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [song, setSong] = useState(null);
  const [notes, setNotes] = useState([]);
  const [mapping, setMapping] = useState([]);
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState('');

  useEffect(() => {
    Promise.all([
      getSong(id).catch(() => null),
      getSongNotes(id),
      getMapping('C', 'paddy'),
    ]).then(([s, n, m]) => {
      setSong(s);
      setNotes(n);
      setMapping(m.holes || []);
    });
  }, [id]);

  const updateNote = (idx, field, value) => {
    setNotes(prev => prev.map((n, i) => i === idx ? { ...n, [field]: value } : n));
  };

  const addNote = () => {
    const lastNote = notes[notes.length - 1];
    const measure = lastNote ? lastNote.measure : 1;
    const position = lastNote ? lastNote.position + 1 : 1;
    setNotes(prev => [...prev, {
      id: 0, measure, position, pitch: 'C4', duration: 'quarter', dot: false, tie: false,
    }]);
  };

  const removeNote = (idx) => {
    setNotes(prev => prev.filter((_, i) => i !== idx));
  };

  const save = async () => {
    setSaving(true);
    setMsg('');
    try {
      const cleaned = notes.map(({ id: _, ...n }) => n);
      await updateSongNotes(id, cleaned);
      setMsg('保存成功');
    } catch {
      setMsg('保存失败');
    } finally {
      setSaving(false);
    }
  };

  if (!song) return <div className="admin-loading">加载中...</div>;

  return (
    <div className="note-editor">
      <div className="editor-header">
        <button className="btn-back" onClick={() => navigate('/admin/songs')}>← 返回</button>
        <h2>{song.title} - 简谱编辑</h2>
        <div className="editor-actions">
          {msg && <span className={msg.includes('成功') ? 'success-text' : 'error-text'}>{msg}</span>}
          <button className="btn btn-primary" onClick={save} disabled={saving}>
            {saving ? '保存中...' : '保存'}
          </button>
        </div>
      </div>

      <div className="preview-section">
        <h3>预览</h3>
        <JianpuRenderer notes={notes} mapping={mapping} timeSignature={song.time_signature} />
      </div>

      <div className="notes-table-section">
        <div className="table-header">
          <h3>音符编辑</h3>
          <button className="btn btn-secondary" onClick={addNote}>+ 添加音符</button>
        </div>
        <div className="notes-table-wrap">
          <table className="notes-table">
            <thead>
              <tr>
                <th>#</th>
                <th>小节</th>
                <th>位置</th>
                <th>音高</th>
                <th>时值</th>
                <th>附点</th>
                <th>连音</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              {notes.map((n, i) => (
                <tr key={i}>
                  <td>{i + 1}</td>
                  <td>
                    <input type="number" min="1" value={n.measure}
                      onChange={e => updateNote(i, 'measure', +e.target.value)} />
                  </td>
                  <td>
                    <input type="number" min="1" value={n.position}
                      onChange={e => updateNote(i, 'position', +e.target.value)} />
                  </td>
                  <td>
                    <input value={n.pitch} onChange={e => updateNote(i, 'pitch', e.target.value)}
                      style={{ width: 60 }} />
                  </td>
                  <td>
                    <select value={n.duration} onChange={e => updateNote(i, 'duration', e.target.value)}>
                      {DURATIONS.map(d => <option key={d} value={d}>{d}</option>)}
                    </select>
                  </td>
                  <td>
                    <input type="checkbox" checked={!!n.dot}
                      onChange={e => updateNote(i, 'dot', e.target.checked)} />
                  </td>
                  <td>
                    <input type="checkbox" checked={!!n.tie}
                      onChange={e => updateNote(i, 'tie', e.target.checked)} />
                  </td>
                  <td>
                    <button className="btn-sm btn-danger" onClick={() => removeNote(i)}>删除</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
