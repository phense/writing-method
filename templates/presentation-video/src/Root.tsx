import React from 'react';
import {Composition} from 'remotion';
import {sceneComponent} from './scenes';
import {FPS, HEIGHT, WIDTH} from './theme';
import {scenes, totalFrames} from './timeline';
import {Video} from './Video';

// "Video" is the deliverable. "Scene-<key>" compositions exist for check
// stills and for working on one scene in the studio.
export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="Video" component={Video} durationInFrames={totalFrames} fps={FPS} width={WIDTH} height={HEIGHT} />
    {scenes.map((scene) => (
      <Composition
        key={scene.key}
        id={`Scene-${scene.key}`}
        component={sceneComponent(scene.key)}
        durationInFrames={scene.frames}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
    ))}
  </>
);
