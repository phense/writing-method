import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';

/** Fades its children in from the given frame. Use with T(i) from useLines. */
export const Appear: React.FC<{from: number; dim?: number; children: React.ReactNode; style?: React.CSSProperties}> = ({
  from,
  dim = 0,
  children,
  style,
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [from, from + 10], [dim, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const y = interpolate(frame, [from, from + 10], [dim ? 0 : 16, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <div style={{opacity, transform: `translateY(${y}px)`, ...style}}>{children}</div>;
};
