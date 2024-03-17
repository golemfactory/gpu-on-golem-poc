import { PropsWithChildren } from 'react';

function Placeholder({ children }: PropsWithChildren) {
  return <div className="relative mx-auto h-[256px] w-[256px] bg-[length:25%]">{children}</div>;
}

export default Placeholder;
