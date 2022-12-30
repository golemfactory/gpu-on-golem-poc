import { useCallback, useEffect, useState } from 'react';
import useWebSocket from 'react-use-websocket';
import { Api } from 'enums/api';
import { Status } from 'enums/status';
import { useFetch, useStatusState } from 'utils/hooks';
import url from 'utils/url';

export function useQueue({ state, dispatch }: useReducerProps) {
  const { forState } = useStatusState(state);

  const [socketUrl, setSocketUrl] = useState<string | null>(null);
  const { lastMessage, readyState } = useWebSocket(socketUrl);
  const [queue, setQueue] = useState({ jobs_in_queue: 0, max_queue_size: 30 });

  const handleFetch = useFetch(dispatch);

  const handleQueue = useCallback(
    (result: { jobs_in_queue: number; max_queue_size: number }) => {
      setQueue(result);

      if (result?.jobs_in_queue === 0) {
        forState([Status.Loading, Status.Ready]) && dispatch({ type: Status.Ready, payload: state.job_id });
        forState([Status.Queued]) && dispatch({ type: Status.Processing, payload: state.job_id });
      } else if (result?.jobs_in_queue === result?.max_queue_size) {
        forState([Status.Loading]) && dispatch({ type: Status.Waiting });
      } else if (result?.jobs_in_queue <= result?.max_queue_size) {
        dispatch({ type: Status.Queued, payload: state.job_id });
      }
    },
    [dispatch, forState, state.job_id],
  );

  useEffect(() => {
    if (forState([Status.Queued]) && state.job_id) {
      handleFetch(url(Api.jobsInQueue, false)).then(setQueue);
    }
  }, [forState, handleFetch, handleQueue, state.job_id]);

  useEffect(() => {
    setSocketUrl(url(Api.jobsInQueue, true));
  }, []);

  useEffect(() => {
    if (lastMessage) {
      const result = JSON.parse(lastMessage.data);

      forState([Status.Loading, Status.Waiting, Status.Queued]) && handleQueue(result);
    }
  }, [readyState, lastMessage, handleQueue, forState]);

  return queue;
}
