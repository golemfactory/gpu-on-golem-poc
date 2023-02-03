import { renderIcon } from 'assets/utils';

function Form({ value, onChange, error, disabled, onSubmit, onExample, onClear }: useFormType) {
  return (
    <form className="relative my-[2.6rem] flex justify-center text-12 text-black" onSubmit={onSubmit}>
      <label
        className={`min-w-[8.4rem] rounded-l-full bg-[#e8e8e8] p-[1.7rem] text-right${
          disabled ? ' text-[#6d6d6d]' : ''
        }`}
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
      >
        Generate
      </button>
      {!disabled && (
        <button
          className="absolute top-[6.2rem] left-[3.1rem] text-10 uppercase underline md:left-[9.6rem]"
          type="button"
          onClick={onExample}
        >
          New Example
        </button>
      )}
      {!!error?.length && (
        <span className="absolute top-[6.2rem] right-0 text-right text-10 text-[#ff0000] md:right-[14.4rem] md:max-w-[50%]">
          {error}
        </span>
      )}
    </form>
  );
}

export default Form;
