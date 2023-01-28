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
  const [queue, setQueue] = useState({ jobs_in_queue: 0, hold_off_user: false });

  const handleFetch = useFetch(dispatch);

  const handleQueue = useCallback(
    (result: { jobs_in_queue: number; hold_off_user: boolean }) => {
      setQueue(result);
      if (result?.hold_off_user) return dispatch({ type: Status.Waiting });

      if (result?.jobs_in_queue === 0) {
        forState([Status.Loading, Status.Ready]) &&
          dispatch({
            type: Status.Ready,
            payload: { job_id: state.job_id },
          });
        forState([Status.Queued]) &&
          dispatch({
            type: !!state.job_id ? Status.Processing : Status.Ready,
            payload: { job_id: state.job_id },
          });
      } else {
        forState([Status.Loading, Status.Ready]) &&
          dispatch({
            type: !!state.job_id ? Status.Queued : Status.Ready,
            payload: { job_id: state.job_id },
          });
      }
    },
    [dispatch, forState, state],
  );

  useEffect(() => {
    if (forState([Status.Queued]) && state.job_id) {
      handleFetch(url(Api.jobsInQueue, false)).then(setQueue);
    }
  }, [forState, handleFetch, state.job_id]);

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
