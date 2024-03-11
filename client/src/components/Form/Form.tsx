import Image from 'next/image';
import { renderIcon } from 'assets/utils';
import { Locked, Terms, useLocked } from 'components';

function Form({ value, onChange, error, disabled, onSubmit, terms }: useFormType) {
  const { limited, locked, until, onUpdate } = useLocked();

  const renderLockTime = (time: string | undefined) => {
    if (!time) return '';

    const seconds = parseInt(time);

    if (isNaN(seconds)) return '';

    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);

    if (hours > 0) {
      return `${hours} hour${hours > 1 ? 's' : ''}`;
    } else if (minutes > 0) {
      return `${minutes} minute${minutes > 1 ? 's' : ''}`;
    } else {
      return `${seconds} second${seconds > 1 ? 's' : ''}`;
    }
  };

  return (
    <>
      <form
        className="relative flex justify-center gap-[0.8rem] bg-white p-[24px] text-12 text-black"
        onSubmit={onSubmit}
      >
        <input
          className="w-full border-[1px] border-solid border-grey bg-[#fafafa] py-[1.7rem] pl-[1.2rem] pr-[2.4rem] font-normal focus:border-blue focus:outline-none focus:ring-1 focus:ring-blue disabled:bg-[#f9f9f9] disabled:text-stone"
          id="phrase"
          name="phrase"
          type="text"
          autoComplete="off"
          value={value}
          onChange={onChange}
          placeholder="Type something"
          disabled={disabled || limited}
        />
        <button
          className="py-[12px] px-[12px] text-14 tracking-[2px] hover:bg-blue hover:text-white focus:outline-none focus:ring disabled:border-grey disabled:bg-grey disabled:text-black md:px-[30px]"
          disabled={disabled || limited}
          onClick={onSubmit}
        >
          <Image
            className="md:hidden"
            src={renderIcon(disabled ? 'playBlack' : 'play')}
            alt="generate image"
            width={24}
            height={24}
          />
          <span className="hidden md:block">Generate</span>
        </button>
        {error?.length && (
          <span className="absolute top-[7.5rem] right-0 text-right text-10 font-light text-[#ff0000] sm:right-[17rem] sm:max-w-[50%]">
            {error}
          </span>
        )}
      </form>
      <div className="mx-auto flex flex-col items-center gap-10 md:flex-row">
        {limited ? (
          <div className="bg-white p-[12px] text-[12px] font-light uppercase">
            <Locked until={until!} onUpdate={onUpdate} />
          </div>
        ) : (
          locked && (
            <div className="bg-white p-[12px] text-[12px] font-light uppercase">
              Use limit:{' '}
              <span className="text-blue">
                {process.env.NEXT_PUBLIC_LOCK_COUNT} per {renderLockTime(process.env.NEXT_PUBLIC_LOCK_TIME_IN_SEC)}
              </span>
            </div>
          )
        )}
        <div className="relative flex min-w-[216px] justify-between">
          {!disabled && <Terms disabled={disabled} terms={terms} />}
        </div>
      </div>
    </>
  );
}

export default Form;
