import { PropsWithChildren } from 'react';
import { useToggle } from 'react-use';
import { renderIcon } from 'assets/utils';

function Tooltip({ type, children }: { type: string } & PropsWithChildren) {
  const [visible, toggle] = useToggle(false);

  return (
    <>
      <button
        className="ml-2 h-[1.2rem] w-[1.2rem] border-transparent bg-transparent bg-contain bg-center bg-no-repeat"
        onClick={toggle}
        style={{ backgroundImage: `url(${renderIcon(type)})` }}
      />
      <div className="relative duration-300">{visible && <div className="ml-8">{children}</div>}</div>
    </>
  );
}

export default Tooltip;
