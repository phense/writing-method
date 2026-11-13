// Single frames at a named second of a scene:
//   node tools/frame.mjs <outdir> <scene>:<second> [...]
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';

const [out, ...specs] = process.argv.slice(2);
if (!out || !specs.length) {
  console.error('usage: node tools/frame.mjs <outdir> <scene>:<second> [...]');
  process.exit(1);
}
fs.mkdirSync(out, {recursive: true});
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
for (const spec of specs) {
  const [key, second] = spec.split(':');
  const composition = await selectComposition({serveUrl, id: `Scene-${key}`});
  const frame = Math.min(Math.round(Number(second) * composition.fps), composition.durationInFrames - 1);
  await renderStill({composition, serveUrl, frame, output: path.join(out, `${key}-${second}s.png`), scale: 0.5});
  process.stdout.write('.');
}
console.log(`\n${specs.length} frames in ${out}`);
