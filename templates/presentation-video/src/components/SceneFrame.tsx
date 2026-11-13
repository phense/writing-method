import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {C, MARGIN, MIN_FONT, sans} from '../theme';
import {chapters, sceneTiming} from '../timeline';
import {Caption} from './Caption';

/**
 * Frame of every scene: fade in and out, the chapter row, the title and the
 * caption. `title` defaults to the scene's chapter; pass `bare` for title
 * and closing cards that show no chapter row.
 */
export const SceneFrame: React.FC<{sceneKey: string; title?: string; bare?: boolean; children?: React.ReactNode}> = ({
  sceneKey,
  title,
  bare,
  children,
}) => {
  const frame = useCurrentFrame();
  const scene = sceneTiming(sceneKey);
  const opacity = interpolate(frame, [0, 10, scene.frames - 10, scene.frames], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const current = chapters.findIndex((c) => c.title === scene.chapter);
  return (
    <AbsoluteFill style={{backgroundColor: C.bg, fontFamily: sans, color: C.text}}>
      <AbsoluteFill style={{opacity}}>
        {!bare && (
          <>
            <div style={{position: 'absolute', left: MARGIN, right: MARGIN, top: MARGIN, display: 'flex', gap: 8}}>
              {chapters.map((c, i) => (
                <div
                  key={c.title}
                  style={{
                    flex: 1,
                    textAlign: 'center',
                    fontSize: MIN_FONT,
                    padding: '4px 12px',
                    whiteSpace: 'nowrap',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    borderRadius: 999,
                    border: `1.5px solid ${i === current ? C.accent : C.border}`,
                    color: i === current ? C.bg : i < current ? C.text : C.dim,
                    background: i === current ? C.accent : 'transparent',
                    fontWeight: i === current ? 700 : 400,
                  }}
                >
                  {c.title}
                </div>
              ))}
            </div>
            <div style={{position: 'absolute', left: MARGIN, top: MARGIN + 66, fontSize: 50, fontWeight: 800}}>
              {title ?? scene.chapter}
            </div>
          </>
        )}
        {children}
        <Caption lines={scene.lines} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
