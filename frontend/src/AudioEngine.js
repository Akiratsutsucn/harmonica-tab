const NOTE_MIDI = {
  C: 0, 'C#': 1, Db: 1, D: 2, 'D#': 3, Eb: 3, E: 4, F: 5,
  'F#': 6, Gb: 6, G: 7, 'G#': 8, Ab: 8, A: 9, 'A#': 10, Bb: 10, B: 11,
};

const DURATION_BEATS = {
  whole: 4, half: 2, quarter: 1, eighth: 0.5, sixteenth: 0.25,
};

function pitchToFreq(pitch) {
  const match = pitch.match(/^([A-G])(#|b)?(\d)$/);
  if (!match) return 440;
  const [, name, accidental, octStr] = match;
  const key = accidental === '#' ? name + '#' : accidental === 'b' ? name + 'b' : name;
  const midi = NOTE_MIDI[key] + (parseInt(octStr) + 1) * 12;
  return 440 * Math.pow(2, (midi - 69) / 12);
}

function noteDuration(duration, dot, bpm) {
  const quarterSec = 60 / bpm;
  let beats = DURATION_BEATS[duration] || 1;
  if (dot) beats *= 1.5;
  return beats * quarterSec;
}

export default class AudioEngine {
  constructor() {
    this._ctx = null;
    this._stopFlag = false;
    this._playing = false;
  }

  _ensureCtx() {
    if (!this._ctx) this._ctx = new AudioContext();
    if (this._ctx.state === 'suspended') this._ctx.resume();
    return this._ctx;
  }

  get playing() { return this._playing; }

  _playTone(freq, duration) {
    const ctx = this._ensureCtx();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.value = freq;
    gain.gain.setValueAtTime(0, ctx.currentTime);
    gain.gain.linearRampToValueAtTime(0.3, ctx.currentTime + 0.02);
    gain.gain.setValueAtTime(0.3, ctx.currentTime + duration - 0.03);
    gain.gain.linearRampToValueAtTime(0, ctx.currentTime + duration);
    osc.connect(gain).connect(ctx.destination);
    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + duration);
  }

  async playSequence(notes, bpm, { speed = 1, onNote, onDone, startMeasure, endMeasure } = {}) {
    this._stopFlag = false;
    this._playing = true;
    const effectiveBpm = bpm * speed;

    let filtered = notes;
    if (startMeasure != null && endMeasure != null) {
      filtered = notes.filter(n => n.measure >= startMeasure && n.measure <= endMeasure);
    }
    const sorted = [...filtered].sort((a, b) => a.measure - b.measure || a.position - b.position);

    for (let i = 0; i < sorted.length; i++) {
      if (this._stopFlag) break;
      const note = sorted[i];
      const freq = pitchToFreq(note.pitch);
      const dur = noteDuration(note.duration, note.dot, effectiveBpm);
      if (onNote) onNote(note, i);
      this._playTone(freq, dur);
      await new Promise(r => setTimeout(r, dur * 1000 + 20));
    }
    this._playing = false;
    if (onDone && !this._stopFlag) onDone();
  }

  stop() {
    this._stopFlag = true;
    this._playing = false;
  }

  destroy() {
    this.stop();
    if (this._ctx) { this._ctx.close(); this._ctx = null; }
  }
}
