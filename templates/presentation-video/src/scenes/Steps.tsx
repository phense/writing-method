import React from 'react';
import {Appear} from '../components/Appear';
import {SceneFrame} from '../components/SceneFrame';
import {C, MARGIN} from '../theme';
import {useLines} from '../timeline';

const STEPS = ['Script', 'Voice', 'Timeline', 'Render'];

// One box per narration line: each lights up when its sentence starts.
export const Steps: React.FC = () => {
  const {T, line} = useLines('steps');
  return (
    <SceneFrame sceneKey="steps">
      <div style={{position: 'absolute', left: MARGIN, right: MARGIN, top: 330, display: 'flex', gap: 36}}>
        {STEPS.map((label, i) => (
          <Appear key={label} from={T(i)} dim={0.25} style={{flex: 1}}>
            <div
              style={{
                height: 300,
                borderRadius: 24,
                background: C.panel,
                border: `3px solid ${line === i ? C.accent : C.border}`,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 18,
              }}
            >
              <div style={{fontSize: 34, color: C.dim}}>{i + 1}</div>
              <div style={{fontSize: 54, fontWeight: 800}}>{label}</div>
            </div>
          </Appear>
        ))}
      </div>
    </SceneFrame>
  );
};
