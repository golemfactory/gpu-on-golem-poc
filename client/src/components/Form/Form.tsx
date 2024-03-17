import Image from 'next/image';
import Link from 'next/link';
import { renderIcon } from 'assets/utils';
import { Locked, useLocked } from 'components';

function Form({ value, onChange, onClear, onExample, error, disabled, onSubmit }: useFormType) {
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
          className="w-full rounded-none border-[1px] border-solid border-grey bg-paper py-[1.7rem] pl-[1.2rem] pr-[2.4rem] font-normal focus:border-blue focus:outline-none focus:ring-1 focus:ring-blue disabled:bg-[#f9f9f9] disabled:text-stone"
          id="phrase"
          name="phrase"
          type="text"
          autoComplete="off"
          value={value}
          onChange={onChange}
          onFocus={onClear}
          onBlur={(e) => {
            if (!Boolean(value) && e.relatedTarget?.id !== 'submit') {
              onExample();
            }
          }}
          placeholder="Enter your prompt"
          disabled={disabled || limited}
        />
        <button
          id="submit"
          className="py-[12px] px-[12px] text-14 tracking-[2px] hover:bg-blue hover:text-white focus:outline-none focus:ring disabled:border-grey disabled:bg-grey disabled:text-black md:px-[30px]"
          disabled={disabled || limited}
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
          <span className="absolute top-[8rem] right-[7.7rem] text-right text-10 font-light text-[#ff0000] sm:right-[18.7rem] sm:max-w-[50%]">
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
        <div className="w-[250px] text-left">
          {!disabled && (
            <span className="text-[12px] font-light uppercase">
              By clicking "Generate" you confirm acceptance of our{' '}
              <Link className="underline" href="/terms">
                Terms of Use
              </Link>
            </span>
          )}
        </div>
      </div>
    </>
  );
}

export default Form;
