import { Status } from 'enums/status';
import { renderIcon } from 'assets/utils';
import { Tooltip } from 'components';
import { useStatusState } from 'utils/hooks';

function Form({ state, value, onChange, error, onSubmit, onExample }: { state: State } & useFormType) {
  const { forState } = useStatusState(state);

  const disabled = !!state.job_id;
  const processing = forState([Status.Processing]);

  return (
    <form className="relative my-[2.6rem] flex justify-center text-12 text-black" onSubmit={onSubmit}>
      <Tooltip
        type="help"
        text="The text you see is just an example. You can give your imagination a try and type whatever comes to your mind.
        One word minimum, but we strongly encourage you to be expressive with your description, as this should get you
        better results. Have fun!"
      />
      <label
        className={`min-w-[8.4rem] rounded-l-full bg-[#e8e8e8] p-[1.7rem] text-right${
          disabled ? ' text-[#6d6d6d]' : ''
        }`}
        htmlFor="phrase"
      >
        Type:
      </label>
      <input
        className="w-full rounded-[0] bg-[#f9f9f9] px-[1.2rem] py-[1.7rem] focus:outline-none focus:ring disabled:bg-[#f9f9f9] disabled:text-stone"
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
        className="min-w-[14.4rem] rounded-r-full bg-[right_2rem_center] bg-no-repeat p-[1.7rem] text-left text-14 focus:outline-none focus:ring disabled:bg-[#6d6d6d]"
        style={processing ? {} : { backgroundImage: `url(${renderIcon('play')})` }}
        disabled={disabled}
      >
        {processing ? 'Generating...' : 'Generate'}
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
