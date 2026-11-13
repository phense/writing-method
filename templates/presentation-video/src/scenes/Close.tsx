import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Appear} from '../components/Appear';
import {SceneFrame} from '../components/SceneFrame';
import {C} from '../theme';
import {useLines} from '../timeline';

export const Close: React.FC = () => {
  const {T} = useLines('close');
  return (
    <SceneFrame sceneKey="close" bare>
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', paddingBottom: 140}}>
        <Appear from={T(0)}>
          <div style={{fontSize: 64, fontWeight: 800, textAlign: 'center'}}>One sentence changed, one sentence voiced.</div>
        </Appear>
        <Appear from={T(1)}>
          <div style={{fontSize: 44, color: C.good, marginTop: 32}}>Have fun building your first video!</div>
        </Appear>
      </AbsoluteFill>
    </SceneFrame>
  );
};
