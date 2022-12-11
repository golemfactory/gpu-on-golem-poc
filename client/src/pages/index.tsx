import { Reducer, useReducer } from 'react';
import { Status } from 'enums/status';
import { Error, Form, Layout, Loader, Process, Queue, Result, useForm, useQueue, useResult } from 'components';

function Main() {
  const reducer = (state: State, action: { type: Status; payload?: string }) => ({
    status: action.type,
    job_id: action.payload,
  });

  const [state, dispatch] = useReducer<Reducer<State, Action>>(reducer, {
    status: Status.Loading,
    job_id: undefined,
  });

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
      <Loader state={state} />
      {[Status.Loading, Status.Waiting, Status.Ready, Status.Queued, Status.Processing].includes(state.status) && (
        <div className="mt-[20rem]">
          <h1 className="mb-[5.7rem] text-34">
            AI image generator supported by the computing power of the{' '}
            <a className="text-blue underline" href="https://www.golem.network/" target="_blank" rel="noreferrer">
              golem.network
            </a>
          </h1>
          <Form state={state} value={value} onExample={onExample} {...form} />
        </div>
      )}
      {[Status.Ready].includes(state.status) && (
        <p className="mt-[5.7rem] text-12">
          We have integrated open-source AI image generator <span className="underline">Stable Diffusion</span> with
          decentralized <span className="underline">golem.network</span> as&nbsp;a&nbsp;backend to showcase its
          computation possibilities with GPU. It is still an early POC rather than full fledged product, but you can
          play around with it and let us know what you think.
        </p>
      )}
      {[Status.Queued].includes(state.status) && <Queue {...queue} />}
      {[Status.Processing].includes(state.status) && <Process status={state.status} progress={data?.progress} />}
      {[Status.Finished].includes(state.status) && <Result data={data} value={value} onReset={handleReset} />}
      {[Status.Error].includes(state.status) && (
        <div className="mt-[20rem]">
          <Error label="Refresh site" onClick={handleReload} />
        </div>
      )}
    </Layout>
  );
}

export default Main;
