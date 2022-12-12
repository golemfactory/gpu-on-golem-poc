import { Status } from 'enums/status';
import { useStatusState } from 'utils/hooks';

function Form({ state, value, onChange, error, onSubmit, onExample }: { state: State } & useFormType) {
  const { forState } = useStatusState(state);

  const disabled = forState([Status.Queued, Status.Processing]);

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
        className="w-full bg-[#f9f9f9] px-[1.2rem] py-[1.7rem] focus:outline-none focus:ring disabled:text-[#9c9c9c]"
        id="phrase"
        name="phrase"
        type="text"
        autoComplete="off"
        value={value}
        onChange={onChange}
        placeholder="Type something or generate new example"
        disabled={disabled}
      />
      <button
        className="min-w-[14.4rem] rounded-r-full p-[1.7rem] text-left text-14 focus:outline-none focus:ring disabled:bg-[#6d6d6d]"
        disabled={disabled}
      >
        {disabled ? 'Generating...' : 'Generate'}
      </button>
      {!disabled && (
        <button
          className="absolute top-[5.8rem] left-0 ml-[8.4rem] text-10 uppercase underline"
          type="button"
          onClick={onExample}
        >
          New Example
        </button>
      )}
      {!!error?.length && (
        <span className="absolute top-[5.8rem] right-0 max-w-[50%] text-right text-[#ff0000]">{error}</span>
      )}
    </form>
  );
}

export default Form;
