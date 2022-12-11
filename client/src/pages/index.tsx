import { Reducer, useEffect, useReducer } from 'react';
import { Api } from 'enums/api';
import { Status } from 'enums/status';
import { Queue } from 'enums/queue';
import { Error, Form, Layout, Loader, Result, useForm, useResult } from 'components';
import url from 'utils/url';

function Main() {
  const reducer = (state: State, action: { type: Status; payload?: string }) => ({
    status: action.type,
    job_id: action.payload,
  });

  const [state, dispatch] = useReducer<Reducer<State, Action>>(reducer, {
    status: Status.Loading,
    job_id: undefined,
  });

  const handleQueue = async () => {
    const response = await fetch(url(Api.jobsInQueue, false));

    if (response.status === 404) return dispatch({ type: Status.Error });

    const result = await response.json();

    if (result.jobs_in_queue < Queue.Max) {
      dispatch({ type: Status.Ready });
    } else {
      dispatch({ type: Status.Waiting });
    }
  };

  useEffect(() => {
    handleQueue().then();
  }, []);

  const { value, onReset, ...form } = useForm(dispatch);

  const { data } = useResult(state, dispatch);

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
          <Form state={state} value={value} {...form} />
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
      {[Status.Queued].includes(state.status) && (
        <>
          <p className="mt-[5.7rem] mb-[2.4rem] text-14">Fun facts:</p>
          <p className="text-18">
            You are now waiting in the queue for your turn. There are 2 turns. Right and left. We have to hire a new
            copywriter… you know anyone?
          </p>
        </>
      )}
      {[Status.Finished].includes(state.status) && <Result data={data} value={value} onReset={onReset} />}
      {[Status.Error].includes(state.status) && (
        <div className="mt-[20rem]">
          <Error label="Refresh site" onClick={handleReload} />
        </div>
      )}
    </Layout>
  );
}

export default Main;
