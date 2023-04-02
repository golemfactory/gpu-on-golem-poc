import { ReactNode } from 'react';
import placeholderPNG from 'assets/placeholder.png';

function Placeholder({ children }: { children?: ReactNode }) {
  return (
    <div
      className="relative mx-auto h-[33.2rem] w-[33.2rem] bg-[length:25%] md:h-[36.2rem] md:w-[36.2rem]"
      style={{ backgroundImage: `url(${placeholderPNG.src})` }}
    >
      {children}
    </div>
  );
}

export default Placeholder;
