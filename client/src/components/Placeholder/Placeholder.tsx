import { ReactNode } from 'react';
import placeholderPNG from 'assets/placeholder.png';

function Placeholder({ children }: { children?: ReactNode }) {
  return (
    <div
      className="mx-auto h-[36.2rem] w-[36.2rem] bg-[length:25%]"
      style={{ backgroundImage: `url(${placeholderPNG.src})` }}
    >
      {children}
    </div>
  );
}

export default Placeholder;
