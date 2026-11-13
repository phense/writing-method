import React from 'react';
import {AbsoluteFill} from 'remotion';
import {SceneFrame} from '../components/SceneFrame';
import {C, MARGIN} from '../theme';
import {sceneTiming} from '../timeline';
import {Close} from './Close';
import {Intro} from './Intro';
import {Steps} from './Steps';

// Scene key (src/scenes.json) -> component. A scene without an entry is shown
// as a placeholder with its message, so a new script renders at once and the
// missing pictures are obvious in the check stills.
const REGISTRY: Record<string, React.FC> = {
  intro: Intro,
  steps: Steps,
  close: Close,
};

const Placeholder: React.FC<{sceneKey: string}> = ({sceneKey}) => (
  <SceneFrame sceneKey={sceneKey}>
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', padding: MARGIN * 2}}>
      <div style={{fontSize: 30, color: C.warn, marginBottom: 20}}>PLACEHOLDER: scene "{sceneKey}" has no picture yet</div>
      <div style={{fontSize: 48, textAlign: 'center'}}>{sceneTiming(sceneKey).message}</div>
    </AbsoluteFill>
  </SceneFrame>
);

export const sceneComponent = (key: string): React.FC => REGISTRY[key] ?? (() => <Placeholder sceneKey={key} />);
