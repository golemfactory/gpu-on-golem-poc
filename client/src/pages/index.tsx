import { Reducer, useReducer } from 'react';
import { Status } from 'enums/status';
import {
  Background,
  Error,
  Form,
  Layout,
  Loader,
  Process,
  Queue,
  Result,
  useForm,
  useQueue,
  useResult,
} from 'components';
import { useStatusState } from 'utils/hooks';

function Main() {
  const reducer = (state: State, action: { type: Status; payload?: string }) => ({
    status: action.type,
    job_id: action.payload,
  });

  const [state, dispatch] = useReducer<Reducer<State, Action>>(reducer, {
    status: Status.Loading,
    job_id: undefined,
  });

  const { forState, notForState } = useStatusState(state);

  const queue = useQueue(state, dispatch);

  const { value, onExample, ...form } = useForm(dispatch);

  const { data, onReset } = useResult(state, dispatch);

  const handleReset = () => {
    dispatch({ type: Status.Ready });
    onExample();
    onReset();
  };

  const handleReload = () => window.location.reload();

  return (
    <Layout>
      {notForState([Status.Finished]) && <Background />}
      <Loader state={state} />
      {notForState([Status.Finished, Status.Error]) && (
        <div className="mt-[20rem]">
          <h1 className="mb-[5.7rem] text-34">
            AI image generator supported by the computing power of the{' '}
            <a
              className="text-blue underline hover:opacity-80"
              href="https://www.golem.network/"
              target="_blank"
              rel="noreferrer"
            >
              golem.network
            </a>
          </h1>
          <Form state={state} value={value} onExample={onExample} {...form} />
        </div>
      )}
      {forState([Status.Ready]) && (
        <p className="mt-[5.7rem] text-12">
          We have integrated open-source AI image generator <span className="underline">Stable Diffusion</span> with
          decentralized <span className="underline">golem.network</span> as&nbsp;a&nbsp;backend to showcase its
          computation possibilities with GPU. It is still an early POC rather than full fledged product, but you can
          play around with it and let us know what you think.
        </p>
      )}
      {forState([Status.Queued]) && <Queue {...queue} />}
      {forState([Status.Processing]) && <Process status={state.status} />}
      {forState([Status.Finished]) && <Result data={data} value={value} onReset={handleReset} />}
      {forState([Status.Error]) && (
        <div className="mt-[20rem]">
          <Error label="Refresh site" onClick={handleReload} />
        </div>
      )}
    </Layout>
  );
}

export default Main;
