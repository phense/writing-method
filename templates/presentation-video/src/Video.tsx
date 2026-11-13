import React from 'react';
import {Html5Audio, Sequence, Series, staticFile} from 'remotion';
import {sceneComponent} from './scenes';
import {s} from './theme';
import {scenes} from './timeline';

// Scenes in script order; each line's sound starts at the frame the timeline
// gives it. A draft timeline has no sound files.
export const Video: React.FC = () => (
  <Series>
    {scenes.map((scene) => {
      const Scene = sceneComponent(scene.key);
      return (
        <Series.Sequence key={scene.key} durationInFrames={scene.frames}>
          <Scene />
          {scene.lines.map((line, i) =>
            line.file ? (
              <Sequence key={i} from={s(line.audio_at)} durationInFrames={s(line.duration) + 2}>
                <Html5Audio src={staticFile(line.file)} />
              </Sequence>
            ) : null,
          )}
        </Series.Sequence>
      );
    })}
  </Series>
);
