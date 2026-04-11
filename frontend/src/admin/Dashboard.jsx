import { useState, useEffect } from 'react';
import { getDashboard } from '../adminApi';

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDashboard().then(setData).catch(() => {}).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="admin-loading">加载中...</div>;
  if (!data) return <div className="admin-error">加载失败</div>;

  const cards = [
    { label: '总曲目', value: data.total_songs, color: '#1677ff' },
    { label: '已审核', value: data.verified_songs, color: '#52c41a' },
    { label: '待审核', value: data.pending_songs, color: '#faad14' },
    { label: '已驳回', value: data.rejected_songs, color: '#ff4d4f' },
    { label: '总任务', value: data.total_tasks, color: '#722ed1' },
    { label: '运行中', value: data.running_tasks, color: '#13c2c2' },
  ];

  return (
    <div className="dashboard">
      <h2>数据概览</h2>
      <div className="stat-grid">
        {cards.map(c => (
          <div className="stat-card" key={c.label}>
            <div className="stat-value" style={{ color: c.color }}>{c.value}</div>
            <div className="stat-label">{c.label}</div>
          </div>
        ))}
      </div>

      {Object.keys(data.source_stats).length > 0 && (
        <div className="source-section">
          <h3>来源分布</h3>
          <div className="source-bars">
            {Object.entries(data.source_stats).map(([source, count]) => (
              <div className="source-bar" key={source}>
                <span className="source-name">{source}</span>
                <div className="bar-track">
                  <div
                    className="bar-fill"
                    style={{ width: `${(count / data.total_songs) * 100}%` }}
                  />
                </div>
                <span className="source-count">{count}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
