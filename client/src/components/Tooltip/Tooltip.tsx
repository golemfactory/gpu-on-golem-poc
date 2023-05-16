import { ReactNode } from 'react';
import { useToggle } from 'react-use';
import { renderIcon } from 'assets/utils';

function Tooltip({ type, children }: { type: string; children: ReactNode }) {
  const [visible, toggle] = useToggle(false);

  return (
    <>
      <button
        className="h-[1.2rem] w-[1.2rem] bg-transparent bg-contain bg-center bg-no-repeat hover:opacity-80"
        onClick={toggle}
        style={{ backgroundImage: `url(${renderIcon(type)})` }}
      />
      <div className="relative duration-300">
        {visible && (
          <div className="b-[#e8e8e8] absolute top-[2.5rem] -right-[1rem] w-[20rem] -translate-y-full">{children}</div>
        )}
      </div>
    </>
  );
}

export default Tooltip;
