import { PropsWithChildren } from 'react';
import placeholderPNG from 'assets/placeholder.png';

function Placeholder({ children }: PropsWithChildren) {
  return (
    <div
      className="relative mx-auto h-[256px] w-[256px] bg-[length:25%]"
      style={{ backgroundImage: `url(${placeholderPNG.src})` }}
    >
      {children}
    </div>
  );
}

export default Placeholder;
