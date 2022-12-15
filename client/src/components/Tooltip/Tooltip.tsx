import { renderIcon } from 'assets/utils';

function Tooltip({ type, text, bottom }: { type: string; text: string; bottom?: boolean }) {
  return (
    <div className="group absolute -top-[2.5rem] right-[1.5rem] duration-300">
      <div
        className="h-[1.8rem] w-[1.8rem] bg-contain bg-center bg-no-repeat hover:opacity-80"
        style={{ backgroundImage: `url(${renderIcon(type)})` }}
      />
      <span
        className={`absolute ${
          bottom ? 'top-[5.7rem]' : '-top-[0.5rem]'
        } right-0 hidden w-[25rem] -translate-y-full rounded-[0.8rem] bg-[#e8e8e8] p-[1rem] text-10 text-black group-hover:flex`}
      >
        {text}
      </span>
    </div>
  );
}

export default Tooltip;
