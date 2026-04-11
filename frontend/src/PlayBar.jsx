import { useState, useCallback } from 'react';

const SPEEDS = [0.5, 0.75, 1, 1.25, 1.5];

export default function PlayBar({ engine, notes, bpm, onNoteHighlight, startMeasure, endMeasure, loop }) {
  const [playing, setPlaying] = useState(false);
  const [speed, setSpeed] = useState(1);
  const [currentIdx, setCurrentIdx] = useState(-1);

  const totalMeasures = notes.length > 0
    ? Math.max(...notes.map(n => n.measure))
    : 0;

  const currentMeasure = currentIdx >= 0 && notes[currentIdx]
    ? notes[currentIdx].measure
    : 0;

  const handlePlay = useCallback(async () => {
    if (!engine || playing) return;
    setPlaying(true);
    const play = async () => {
      await engine.playSequence(notes, bpm, {
        speed,
        startMeasure,
        endMeasure,
        onNote: (note, idx) => {
          setCurrentIdx(idx);
          if (onNoteHighlight) onNoteHighlight(note, idx);
        },
        onDone: () => {
          if (loop && !engine._stopFlag) {
            play();
          } else {
            setPlaying(false);
            setCurrentIdx(-1);
            if (onNoteHighlight) onNoteHighlight(null, -1);
          }
        },
      });
    };
    await play();
  }, [engine, notes, bpm, speed, playing, onNoteHighlight, startMeasure, endMeasure, loop]);

  const handleStop = useCallback(() => {
    if (engine) engine.stop();
    setPlaying(false);
    setCurrentIdx(-1);
    if (onNoteHighlight) onNoteHighlight(null, -1);
  }, [engine, onNoteHighlight]);

  const cycleSpeed = useCallback(() => {
    setSpeed(prev => {
      const idx = SPEEDS.indexOf(prev);
      return SPEEDS[(idx + 1) % SPEEDS.length];
    });
  }, []);

  return (
    <div className="play-bar">
      <button className="play-btn" onClick={playing ? handleStop : handlePlay}>
        {playing ? '⏹' : '▶'}
      </button>
      <div className="play-progress">
        <span>{currentMeasure} / {totalMeasures}</span>
      </div>
      <button className="speed-btn" onClick={cycleSpeed}>
        {speed}x
      </button>
    </div>
  );
}
