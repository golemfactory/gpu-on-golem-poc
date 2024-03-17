import { PropsWithChildren } from 'react';

function Progress({ width, children }: { width: number } & PropsWithChildren) {
  return (
    <div className="relative h-[48px] w-full border-[1px] border-solid border-grey bg-paper">
      <div className="h-[47px] bg-grey" style={{ maxWidth: `${width}%` }} />
      {children}
    </div>
  );
}

export default Progress;
