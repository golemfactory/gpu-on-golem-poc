import { Reducer, useReducer } from 'react';
import { Status } from 'enums/status';
import {
  Background,
  Error,
  Form,
  Hero,
  Layout,
  Loader,
  Queue,
  Result,
  useForm,
  useNodes,
  useQueue,
  useResult,
} from 'components';
import { useStatusState } from 'utils/hooks';

function Main() {
  const reducer = (state: State, action: Action) => ({
    status: action.type,
    job_id: action.payload,
    error: action.error,
  });

  const [state, dispatch] = useReducer<Reducer<State, Action>>(reducer, {
    status: Status.Loading,
    job_id: undefined,
    error: undefined,
  });

  const { forState, notForState } = useStatusState(state);

  const queue = useQueue({ state, dispatch });

  const { value, onExample, ...form } = useForm({ state, dispatch });

  const { data, onReset } = useResult({ state, dispatch });

  const handleReset = () => {
    dispatch({ type: Status.Ready });
    onExample();
    onReset();
  };

  const handleReload = () => window.location.reload();

  const nodes = useNodes({ state, dispatch });

  return (
    <Layout>
      {notForState([Status.Processing, Status.Finished, Status.Blocked]) && <Background />}
      <Loader state={state} />
      {notForState([Status.Processing, Status.Finished, Status.Blocked, Status.Error]) && (
        <Hero>
          <Form value={value} onExample={onExample} {...form} />
        </Hero>
      )}
      {forState([Status.Ready]) && (
        <p className="mt-[5.7rem] text-12">
          We have integrated the AI Stable Diffusion image generator with the decentralized Golem Network to showcase
          its computation possibilities with a GPU.
          <br />
          <br />
          We are currently using limited resources - 2 computers with a GPU, therefore, you may encounter difficulties
          using the application.
          <br />
          <br />
          Want to give us feedback? Go to our Discord and get involved!
        </p>
      )}
      {forState([Status.Queued]) && <Queue {...queue} />}
      {forState([Status.Processing, Status.Finished, Status.Blocked]) && (
        <Result state={state} data={data} value={value} onReset={handleReset} nodes={nodes} />
      )}
      {forState([Status.Error]) && (
        <Error
          {...(state.error === 429 && { heading: 'Too many requests.', text: 'Please try again in few minutes.' })}
          button={{ label: 'Refresh site', onClick: handleReload }}
        />
      )}
    </Layout>
  );
}

export default Main;
