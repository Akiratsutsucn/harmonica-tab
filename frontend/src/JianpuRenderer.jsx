import { useMemo } from 'react';

/**
 * Renders jianpu (numbered musical notation) with harmonica hole annotations.
 *
 * Props:
 *   notes: array of {measure, position, pitch, duration, dot, tie}
 *   mapping: array of hole mappings from API
 *   timeSignature: string like '4/4'
 */
export default function JianpuRenderer({ notes = [], mapping = [], timeSignature = '4/4' }) {
  // Build a lookup: pitch -> {hole, action}
  const holeLookup = useMemo(() => {
    const lookup = {};
    if (!mapping.length) return lookup;
    for (const h of mapping) {
      const blowNote = h.blow.note;
      const drawNote = h.draw.note;
      if (!lookup[blowNote]) lookup[blowNote] = { hole: h.hole, action: 'blow' };
      if (!lookup[drawNote]) lookup[drawNote] = { hole: h.hole, action: 'draw' };
    }
    return lookup;
  }, [mapping]);

  // Group notes by measure
  const measures = useMemo(() => {
    const map = {};
    for (const n of notes) {
      if (!map[n.measure]) map[n.measure] = [];
      map[n.measure].push(n);
    }
    return Object.entries(map)
      .sort(([a], [b]) => Number(a) - Number(b))
      .map(([, ns]) => ns.sort((a, b) => a.position - b.position));
  }, [notes]);

  if (!notes.length) {
    return <div className="empty-state"><div className="icon">🎵</div><p>暂无曲谱数据</p></div>;
  }

  return (
    <div className="sheet-canvas-wrap">
      <div className="measure-row">
        {measures.map((measureNotes, mi) => (
          <div className="measure" key={mi}>
            {measureNotes.map((note, ni) => (
              <NoteColumn key={ni} note={note} holeLookup={holeLookup} />
            ))}
          </div>
        ))}
      </div>
      <div className="legend">
        <div className="legend-item">
          <div className="legend-dot" style={{ background: 'var(--blow-color)' }} />
          <span>吹 ↑</span>
        </div>
        <div className="legend-item">
          <div className="legend-dot" style={{ background: 'var(--draw-color)' }} />
          <span>吸 ↓</span>
        </div>
      </div>
    </div>
  );
}

const NOTE_NAMES = { C: '1', D: '2', E: '3', F: '4', G: '5', A: '6', B: '7' };

function pitchToJianpu(pitch) {
  // Parse pitch like "C4", "C#5", "Bb3"
  const match = pitch.match(/^([A-G])(#|b)?(\d)$/);
  if (!match) return { num: '0', octaveDots: 0, sharp: false };
  const [, name, accidental, octStr] = match;
  const octave = parseInt(octStr);
  return {
    num: NOTE_NAMES[name] || '0',
    octaveDots: octave - 4, // 4 = middle octave
    sharp: accidental === '#',
    flat: accidental === 'b',
  };
}

function durationLines(duration) {
  // eighth = 1 line, sixteenth = 2 lines
  if (duration === 'eighth') return 1;
  if (duration === 'sixteenth') return 2;
  return 0;
}

function NoteColumn({ note, holeLookup }) {
  const jp = pitchToJianpu(note.pitch);
  const holeInfo = holeLookup[note.pitch];
  const lines = durationLines(note.duration);

  return (
    <div className="note-col">
      {/* Octave dots above */}
      {jp.octaveDots > 0 && (
        <div className="octave-dot above">
          {'·'.repeat(jp.octaveDots)}
        </div>
      )}

      {/* Jianpu number */}
      <div className={`jianpu-num${jp.sharp ? ' sharp' : ''}`}>
        {jp.flat && <span style={{ fontSize: 12, position: 'absolute', left: -8, top: -2 }}>♭</span>}
        {jp.num}
        {note.dot ? '·' : ''}
      </div>

      {/* Octave dots below */}
      {jp.octaveDots < 0 && (
        <div className="octave-dot below">
          {'·'.repeat(Math.abs(jp.octaveDots))}
        </div>
      )}

      {/* Duration underlines (eighth, sixteenth) */}
      {Array.from({ length: lines }).map((_, i) => (
        <div className="duration-line" key={i} />
      ))}

      {/* Harmonica hole annotation */}
      {holeInfo ? (
        <div className={`hole-tag ${holeInfo.action}`}>
          {holeInfo.hole}{holeInfo.action === 'blow' ? '↑' : '↓'}
        </div>
      ) : (
        <div className="hole-tag" style={{ opacity: 0.3 }}>-</div>
      )}
    </div>
  );
}
