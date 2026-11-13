import {useCurrentFrame} from 'remotion';
import timeline from './timeline.json';
import {s} from './theme';

// Everything about time comes from timeline.json, which tools/timeline.py
// derives from the measured sound. Never write a second or frame number for
// "when" into a scene: anchor animations to line starts with `useLines`.

export type Line = {
  text: string;
  show: boolean;
  file: string | null;
  at: number;
  audio_at: number;
  speech_start: number;
  speech_end: number;
  slot: number;
  duration: number;
};
export type SceneTiming = {
  key: string;
  chapter: string;
  message: string;
  start: number;
  start_frame: number;
  length: number;
  frames: number;
  lines: Line[];
};

export const scenes = timeline.scenes as SceneTiming[];
export const chapters = timeline.chapters as {title: string; start: number}[];
export const totalFrames = timeline.total_frames;
export const isDraft = Boolean((timeline as {draft?: boolean}).draft);

export const sceneTiming = (key: string): SceneTiming => {
  const scene = scenes.find((x) => x.key === key);
  if (!scene) throw new Error(`scene ${key} is not in timeline.json; run tools/timeline.py`);
  return scene;
};

/**
 * Timing helpers for one scene.
 *   const {T, line, on} = useLines('steps');
 *   T(2)        frame at which line 2 starts
 *   T(2, 0.4)   0.4 s after line 2 starts
 *   line        index of the line being shown now (-1 before the first)
 *   on(2)       true from the start of line 2 onward
 */
export const useLines = (key: string) => {
  const frame = useCurrentFrame();
  const lines = sceneTiming(key).lines;
  const T = (index: number, offset = 0) => s(lines[Math.min(index, lines.length - 1)].at + offset);
  const line = lines.reduce((acc, l, i) => (frame >= s(l.at) ? i : acc), -1);
  const on = (index: number, offset = 0) => frame >= T(index, offset);
  return {T, line, on, lines, frame};
};
