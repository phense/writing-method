import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Appear} from '../components/Appear';
import {SceneFrame} from '../components/SceneFrame';
import {C} from '../theme';
import {useLines} from '../timeline';

export const Intro: React.FC = () => {
  const {T} = useLines('intro');
  return (
    <SceneFrame sceneKey="intro" bare>
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', paddingBottom: 140}}>
        <Appear from={T(0)}>
          <div style={{fontSize: 84, fontWeight: 800, textAlign: 'center'}}>How a presentation video is built</div>
        </Appear>
        <Appear from={T(1)}>
          <div style={{fontSize: 40, color: C.dim, marginTop: 28}}>Drawn from a script. Nothing is filmed.</div>
        </Appear>
      </AbsoluteFill>
    </SceneFrame>
  );
};
