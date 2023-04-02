import { ReactNode } from 'react';

function Progress({ width, children }: { width: number; children: ReactNode }) {
  return (
    <div className="progress-bar">
      <div className="progress-bar-indicator" style={{ maxWidth: `calc(${width}% - 0.4rem)` }} />
      {children}
    </div>
  );
}

export default Progress;
