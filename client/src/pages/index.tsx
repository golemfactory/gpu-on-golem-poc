import { useEffect, useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
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
import gaEvent from 'lib/ga';
import { selectJobId } from 'slices/data';
import { selectError } from 'slices/error';
import { resetQueue } from 'slices/queue';
import { selectStatus, setStatus } from 'slices/status';
import { useStatusState } from 'utils/hooks';

function Main() {
  const dispatch = useDispatch();

  const error = useSelector(selectError);
  const job_id = useSelector(selectJobId);
  const status = useSelector(selectStatus);

  const { forState, notForState } = useStatusState();

  useQueue();
  useNodes();
  const { value, onExample, ...form } = useForm();
  const { onReset } = useResult();

  const start_queued = useRef<number>();
  const stop_queued = useRef<number>();

  const start_processing = useRef<number>();
  const stop_processing = useRef<number>();

  useEffect(() => {
    if (!!job_id && forState([Status.Queued])) {
      start_queued.current = Date.now();
    } else if (!!job_id && forState([Status.Processing])) {
      stop_queued.current = Date.now();
      start_processing.current = Date.now();
    } else if (!!job_id && forState([Status.Finished, Status.Blocked])) {
      stop_processing.current = Date.now();
    } else {
      start_queued.current = undefined;
      stop_queued.current = undefined;
      start_processing.current = undefined;
      stop_processing.current = undefined;
    }
  }, [job_id, status]);

  useEffect(() => {
    if (forState([Status.Finished, Status.Blocked])) {
      // @ts-ignore
      const spent_in_queue = (stop_queued.current - start_queued.current) / 1000;
      // @ts-ignore
      const spent_generating = (stop_processing.current - start_processing.current) / 1000;

      gaEvent('txt2img_generated', {
        spent_in_queue,
        spent_generating,
        job_id,
        is_blocked: !!Status.Blocked,
      });
    }
  }, [forState, status]);

  const handleReset = () => {
    dispatch(setStatus(Status.Ready));
    dispatch(resetQueue());
    onExample();
    onReset();
  };

  const handleReload = () => window.location.reload();

  return (
    <Layout>
      {notForState([Status.Processing, Status.Finished, Status.Blocked]) && <Background />}
      <Loader />
      {notForState([Status.Processing, Status.Finished, Status.Blocked, Status.Error]) && (
        <Hero>
          <Form value={value} onExample={onExample} {...form} />
        </Hero>
      )}
      {forState([Status.Ready]) && (
        <p className="mt-[5.7rem] text-12">
          We have integrated the AI Stable Diffusion image generator with the Golem Network to showcase its computation
          possibilities with a GPU. We are currently using limited resources - 2 computers with a GPU, therefore, you
          may encounter difficulties using the application.
        </p>
      )}
      {forState([Status.Queued]) && <Queue />}
      {forState([Status.Processing, Status.Finished, Status.Blocked]) && <Result value={value} onReset={handleReset} />}
      {forState([Status.Error]) && (
        <Error
          {...(error === 429 && { heading: 'Too many requests.', text: 'Please try again in few minutes.' })}
          {...(error === 503 && { heading: 'No available nodes.', text: 'Please try again in few minutes.' })}
          button={{ label: 'Refresh site', onClick: handleReload }}
        />
      )}
    </Layout>
  );
}

export default Main;
