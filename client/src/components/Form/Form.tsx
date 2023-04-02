import { twMerge } from 'tailwind-merge';
import { renderIcon } from 'assets/utils';
import { Checkbox } from 'components';

function Form({ value, onChange, error, disabled, onSubmit, onExample, onClear, terms }: useFormType) {
  return (
    <>
      <form className="relative my-[2.6rem] flex justify-center text-12 text-black" onSubmit={onSubmit}>
        <label
          className={twMerge(
            'min-w-[8.4rem] rounded-l-full bg-[#e8e8e8] p-[1.7rem] text-right',
            disabled && 'text-[#6d6d6d]',
          )}
          htmlFor="phrase"
        >
          Type:
        </label>
        <input
          className="w-full rounded-[0] bg-[#f9f9f9] py-[1.7rem] pl-[1.2rem] pr-[2.4rem] focus:outline-none focus:ring disabled:bg-[#f9f9f9] disabled:text-stone"
          id="phrase"
          name="phrase"
          type="text"
          autoComplete="off"
          value={value}
          onChange={onChange}
          placeholder="Type something or generate new example"
          disabled={disabled}
        />
        {!!value && !disabled && (
          <button
            className="absolute top-[1.7rem] right-[15rem] h-[2rem] w-[2rem] bg-center bg-no-repeat"
            type="button"
            style={{ backgroundImage: `url(${renderIcon('clear')})` }}
            onClick={onClear}
          />
        )}
        <button
          className="min-w-[14.4rem] rounded-r-full bg-[right_2rem_center] bg-no-repeat p-[1.7rem] text-left text-14 focus:outline-none focus:ring disabled:bg-[#6d6d6d]"
          style={{ backgroundImage: `url(${renderIcon('play')})` }}
          disabled={disabled}
          onClick={onSubmit}
        >
          Generate
        </button>
        {error?.length && (
          <span className="absolute top-[6.2rem] right-0 text-right text-10 text-[#ff0000] sm:right-[15.4rem] sm:max-w-[50%]">
            {error}
          </span>
        )}
      </form>
      {!disabled && (
        <div className="relative flex justify-between sm:ml-[3rem] sm:-mt-[1.8rem] sm:ml-[8.4rem] sm:mr-[14.4rem]">
          <Checkbox
            name="terms"
            label="I accept the"
            link="Terms of Use"
            href="/terms"
            disabled={disabled}
            {...terms}
          />
          <button
            className="text-left uppercase underline sm:translate-x-full sm:-translate-y-[0.1rem]"
            type="button"
            onClick={onExample}
          >
            New Example
          </button>
        </div>
      )}
    </>
  );
}

export default Form;
