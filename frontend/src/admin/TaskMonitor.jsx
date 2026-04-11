import { useState, useEffect } from 'react';
import { getTasks, submitAIGenerate, submitCrawl } from '../adminApi';

const STATUS_COLORS = {
  pending: '#faad14',
  running: '#1677ff',
  done: '#52c41a',
  failed: '#ff4d4f',
};

const STATUS_LABELS = {
  pending: '等待中',
  running: '运行中',
  done: '已完成',
  failed: '失败',
};

export default function TaskMonitor() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState('');

  const load = () => {
    setLoading(true);
    const params = {};
    if (filterStatus) params.status = filterStatus;
    getTasks(params).then(setTasks).finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, [filterStatus]);

  // Auto-refresh every 5s
  useEffect(() => {
    const timer = setInterval(load, 5000);
    return () => clearInterval(timer);
  }, [filterStatus]);

  return (
    <div className="task-monitor">
      <div className="manager-header">
        <h2>任务监控</h2>
        <button className="btn btn-secondary" onClick={load}>刷新</button>
      </div>

      <div className="filters">
        <select value={filterStatus} onChange={e => setFilterStatus(e.target.value)}>
          <option value="">全部状态</option>
          <option value="pending">等待中</option>
          <option value="running">运行中</option>
          <option value="done">已完成</option>
          <option value="failed">失败</option>
        </select>
      </div>

      {loading && tasks.length === 0 ? (
        <div className="admin-loading">加载中...</div>
      ) : (
        <div className="song-table">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>类型</th>
                <th>状态</th>
                <th>参数</th>
                <th>结果</th>
                <th>创建时间</th>
              </tr>
            </thead>
            <tbody>
              {tasks.map(t => (
                <tr key={t.id}>
                  <td>{t.id}</td>
                  <td>{t.type}</td>
                  <td>
                    <span className="status-tag" style={{ color: STATUS_COLORS[t.status] }}>
                      {STATUS_LABELS[t.status] || t.status}
                    </span>
                  </td>
                  <td className="json-cell">{formatParams(t.params)}</td>
                  <td className="json-cell">
                    {t.result?.error ? (
                      <span className="error-text">{t.result.error}</span>
                    ) : (
                      formatResult(t.result)
                    )}
                  </td>
                  <td>{t.created_at?.replace('T', ' ').slice(0, 19)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {tasks.length === 0 && <div className="empty">暂无任务</div>}
        </div>
      )}
    </div>
  );
}

function formatParams(params) {
  if (!params || typeof params !== 'object') return '-';
  const { content, ...rest } = params; // exclude large content
  const keys = Object.keys(rest);
  if (keys.length === 0) return '-';
  return keys.map(k => `${k}: ${rest[k]}`).join(', ');
}

function formatResult(result) {
  if (!result || typeof result !== 'object') return '-';
  const keys = Object.keys(result);
  if (keys.length === 0) return '-';
  return keys.map(k => `${k}: ${JSON.stringify(result[k]).slice(0, 50)}`).join(', ');
}
