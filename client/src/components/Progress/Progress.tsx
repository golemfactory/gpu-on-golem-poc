import { ReactNode } from 'react';

function Progress({ width, children }: { width: number; children: ReactNode }) {
  return (
    <div
      className="relative my-[1rem] mx-[2rem] h-[1.2rem] rounded-full bg-[#e7edf3]"
      style={{ width: 'calc(100% - 4rem)' }}
    >
      <div
        className="mx-[0.2rem] h-[0.8rem] translate-y-[0.2rem] rounded-full bg-blue"
        style={{ width: `calc(${width}% - 0.4rem)` }}
      />
      {children}
    </div>
  );
}

export default Progress;
