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
