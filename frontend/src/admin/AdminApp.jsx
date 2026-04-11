import { useState, useCallback } from 'react';
import { Routes, Route, NavLink, useNavigate } from 'react-router-dom';
import AdminLogin from './AdminLogin';
import Dashboard from './Dashboard';
import SongManager from './SongManager';
import NoteEditor from './NoteEditor';
import TaskMonitor from './TaskMonitor';
import BatchImport from './BatchImport';
import './admin.css';

const NAV_ITEMS = [
  { path: '', label: '概览', icon: '📊' },
  { path: 'songs', label: '歌曲', icon: '🎵' },
  { path: 'tasks', label: '任务', icon: '⚙️' },
  { path: 'import', label: '导入', icon: '📥' },
];

export default function AdminApp() {
  const [authed, setAuthed] = useState(() => !!localStorage.getItem('admin_token'));
  const navigate = useNavigate();

  const logout = useCallback(() => {
    localStorage.removeItem('admin_token');
    setAuthed(false);
  }, []);

  if (!authed) {
    return <AdminLogin onLogin={() => setAuthed(true)} />;
  }

  return (
    <div className="admin-layout">
      <nav className="admin-sidebar">
        <div className="sidebar-header">
          <h3>🎵 口琴管理</h3>
        </div>
        <div className="nav-items">
          {NAV_ITEMS.map(item => (
            <NavLink
              key={item.path}
              to={`/admin/${item.path}`}
              end={item.path === ''}
              className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}
            >
              <span className="nav-icon">{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </div>
        <div className="sidebar-footer">
          <button className="logout-btn" onClick={logout}>退出登录</button>
          <button className="back-btn" onClick={() => navigate('/')}>返回前台</button>
        </div>
      </nav>
      <main className="admin-content">
        <Routes>
          <Route index element={<Dashboard />} />
          <Route path="songs" element={<SongManager />} />
          <Route path="songs/:id/notes" element={<NoteEditor />} />
          <Route path="tasks" element={<TaskMonitor />} />
          <Route path="import" element={<BatchImport />} />
        </Routes>
      </main>
    </div>
  );
}
