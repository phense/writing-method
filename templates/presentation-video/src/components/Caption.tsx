import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {C, MARGIN, MIN_FONT, mono, s} from '../theme';
import {Line} from '../timeline';

// Text between backticks is shown as code.
const Rich: React.FC<{text: string}> = ({text}) => (
  <>
    {text.split('`').map((part, i) =>
      i % 2 ? (
        <span key={i} style={{fontFamily: mono, color: C.accent}}>
          {part}
        </span>
      ) : (
        <React.Fragment key={i}>{part}</React.Fragment>
      ),
    )}
  </>
);

/** The spoken line as a caption bar. A caption never changes while it is read. */
export const Caption: React.FC<{lines: Line[]}> = ({lines}) => {
  const frame = useCurrentFrame();
  const index = lines.reduce((acc, l, i) => (frame >= s(l.at) ? i : acc), -1);
  if (index < 0 || !lines[index].show) return null;
  const local = frame - s(lines[index].at);
  const opacity = interpolate(local, [0, 8], [0, 1], {extrapolateRight: 'clamp'});
  const y = interpolate(local, [0, 8], [12, 0], {extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', left: MARGIN, right: MARGIN, bottom: MARGIN, display: 'flex', justifyContent: 'center'}}>
      <div
        style={{
          maxWidth: 1640,
          padding: '20px 36px',
          borderRadius: 18,
          background: 'rgba(15,23,42,0.94)',
          border: `1.5px solid ${C.border}`,
          fontSize: Math.max(32, MIN_FONT),
          lineHeight: 1.4,
          textAlign: 'center',
          opacity,
          transform: `translateY(${y}px)`,
        }}
      >
        <Rich text={lines[index].text} />
      </div>
    </div>
  );
};
