// Check stills: one frame per narration line, taken late in the line's slot.
//   node tools/stills.mjs <outdir> [scene ...]
// Writes <outdir>/<scene>-<nn>.png at half size and <outdir>/stills.json,
// the inspection list: every still starts as "inspected": false and the
// review is not passed until each one was looked at.
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';

const [out, ...only] = process.argv.slice(2);
if (!out) {
  console.error('usage: node tools/stills.mjs <outdir> [scene ...]');
  process.exit(1);
}
const timelinePath = path.resolve('src/timeline.json');
if (!fs.existsSync(timelinePath)) {
  console.error('src/timeline.json is missing; run python3 tools/timeline.py');
  process.exit(1);
}
const timeline = JSON.parse(fs.readFileSync(timelinePath, 'utf8'));
if (timeline.draft) console.warn('DRAFT timeline: stills show estimated timing, not the voiced one');
const manifestPath = path.resolve('src/audio-manifest.json');
if (!timeline.draft && fs.existsSync(manifestPath) && fs.statSync(manifestPath).mtimeMs > fs.statSync(timelinePath).mtimeMs) {
  console.error('src/timeline.json is older than the sound manifest; run python3 tools/timeline.py');
  process.exit(1);
}
fs.mkdirSync(out, {recursive: true});
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const list = [];
for (const scene of timeline.scenes) {
  if (only.length && !only.includes(scene.key)) continue;
  const composition = await selectComposition({serveUrl, id: `Scene-${scene.key}`});
  for (const [i, line] of scene.lines.entries()) {
    const frame = Math.min(Math.round((line.at + 0.85 * line.slot) * timeline.fps), composition.durationInFrames - 1);
    const file = `${scene.key}-${String(i).padStart(2, '0')}.png`;
    await renderStill({composition, serveUrl, frame, output: path.join(out, file), scale: 0.5});
    list.push({file, scene: scene.key, line: i, text: line.text, inspected: false, finding: null});
    process.stdout.write('.');
  }
}
// keep earlier inspection marks of stills that were not rendered again
const listPath = path.join(out, 'stills.json');
const earlier = fs.existsSync(listPath) ? JSON.parse(fs.readFileSync(listPath, 'utf8')) : [];
const fresh = new Set(list.map((x) => x.file));
const current = new Set(
  timeline.scenes.flatMap((scene) => scene.lines.map((_, i) => `${scene.key}-${String(i).padStart(2, '0')}.png`)),
);
const merged = [...earlier.filter((x) => !fresh.has(x.file) && current.has(x.file)), ...list].sort((a, b) =>
  a.file.localeCompare(b.file),
);
fs.writeFileSync(listPath, JSON.stringify(merged, null, 2) + '\n');
console.log(`\n${list.length} stills in ${out}; mark each as inspected in ${listPath}`);
