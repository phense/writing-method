import {loadFont as loadSans} from '@remotion/google-fonts/Inter';
import {loadFont as loadMono} from '@remotion/google-fonts/JetBrainsMono';
import timeline from './timeline.json';

// Font coverage: Latin and Latin Extended only. Arrows, symbols and emoji
// (for example ⏺ ⏱ ✓) are NOT in these fonts and render as empty boxes or
// not at all. Draw such marks as shapes, or add a font that has them, and
// look at the check still of every line that uses one.
const sansFont = loadSans('normal', {weights: ['400', '600', '800'], subsets: ['latin', 'latin-ext']});
const monoFont = loadMono('normal', {weights: ['400', '700'], subsets: ['latin', 'latin-ext']});

export const sans = `${sansFont.fontFamily}, sans-serif`;
export const mono = `${monoFont.fontFamily}, monospace`;

// Size and legibility limits come from the video profile, through the timeline.
const picture = timeline.picture;
export const FPS = timeline.fps;
export const WIDTH = picture.width;
export const HEIGHT = picture.height;
/** Frames for a number of seconds. */
export const s = (seconds: number) => Math.round(seconds * FPS);

// Legibility rules of the method. Keep on-screen text at or above MIN_FONT
// and inside MARGIN: use these constants, do not write smaller numbers.
// Contrast of at least 4.5:1 against the background is checked by eye on the
// check stills; no tool measures it.
export const MIN_FONT = picture.min_font_px;
export const MARGIN = picture.margin_px;

// Replace with the house colours named in the video profile's branding.
export const C = {
  bg: '#0f172a',
  panel: '#1e293b',
  border: '#334155',
  text: '#f1f5f9',
  dim: '#94a3b8',
  accent: '#38bdf8',
  good: '#4ade80',
  warn: '#fbbf24',
};
