import Image from 'next/image';
import { renderIcon } from 'assets/utils';
import { Terms } from 'components';

function Form({ value, onChange, error, disabled, onSubmit, terms }: useFormType) {
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
          disabled={disabled}
        />
        <button
          className="py-[12px] px-[12px] text-14 tracking-[2px] hover:bg-blue hover:text-white focus:outline-none focus:ring disabled:border-grey disabled:bg-grey disabled:text-black md:px-[30px]"
          disabled={disabled}
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
      {!disabled && (
        <div className="relative mx-auto flex justify-between">
          <Terms disabled={disabled} terms={terms} />
        </div>
      )}
    </>
  );
}

export default Form;
