import { useState } from 'react';
import { submitImport } from '../adminApi';

export default function BatchImport() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    if (!file) return;
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const res = await submitImport(file);
      setResult(res);
    } catch (e) {
      setError('导入失败: ' + (e.response?.data?.detail || e.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="batch-import">
      <h2>批量导入</h2>

      <div className="import-info">
        <h3>支持格式</h3>
        <div className="format-cards">
          <div className="format-card">
            <h4>JSON</h4>
            <pre>{`[{
  "title": "歌名",
  "artist": "歌手",
  "key": "C",
  "time_signature": "4/4",
  "bpm": 120,
  "notes": [
    {"measure": 1, "position": 1,
     "pitch": "C4", "duration": "quarter"}
  ]
}]`}</pre>
          </div>
          <div className="format-card">
            <h4>CSV</h4>
            <pre>{`title,artist,key,time_signature,bpm,notation
小星星,儿歌,C,4/4,100,1 1 5 5 | 6 6 5 - | 4 4 3 3 | 2 2 1 -`}</pre>
          </div>
        </div>
      </div>

      <div className="upload-area">
        <input
          type="file"
          accept=".json,.csv"
          onChange={e => setFile(e.target.files[0])}
        />
        <button
          className="btn btn-primary"
          onClick={handleSubmit}
          disabled={!file || loading}
        >
          {loading ? '导入中...' : '开始导入'}
        </button>
      </div>

      {error && <div className="error-msg">{error}</div>}

      {result && (
        <div className="import-result">
          <p>任务已提交 (ID: {result.task_id})</p>
          <p>请在任务监控中查看进度</p>
        </div>
      )}
    </div>
  );
}
