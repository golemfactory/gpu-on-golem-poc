import { useCallback, useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import useWebSocket from 'react-use-websocket';
import { Api } from 'enums/api';
import { Status } from 'enums/status';
import { setQueue } from 'slices/queue';
import { setStatus } from 'slices/status';
import { useStatusState } from 'utils/hooks';
import url from 'utils/url';

export function useQueue({ state, dispatch }: useReducerProps) {
  const appDispatch = useDispatch();

  const { forState } = useStatusState();

  const [socketUrl, setSocketUrl] = useState<string | null>(null);
  const { lastMessage, readyState, getWebSocket } = useWebSocket(socketUrl);

  const handleQueue = useCallback(
    (result: { jobs_in_queue: number; hold_off_user: boolean }) => {
      const { hold_off_user, ...args } = result;

      if (hold_off_user) return appDispatch(setStatus(Status.Waiting));

      if (result?.jobs_in_queue === 0) {
        forState([Status.Loading, Status.Ready]) && dispatch({ payload: { job_id: state.job_id } });
        forState([Status.Loading, Status.Ready]) && appDispatch(setStatus(Status.Ready));
        forState([Status.Loading, Status.Ready]) && !state.job_id && appDispatch(setQueue(args));
      } else {
        forState([Status.Loading, Status.Ready]) &&
          appDispatch(setStatus(!!state.job_id ? Status.Queued : Status.Ready));
        forState([Status.Loading, Status.Ready]) && dispatch({ payload: { job_id: state.job_id } });
      }
    },
    [dispatch, forState, state],
  );

  useEffect(() => {
    setSocketUrl(url(Api.jobsInQueue, true));
  }, []);

  useEffect(() => {
    if (lastMessage) {
      const result = JSON.parse(lastMessage.data);

      forState([Status.Loading, Status.Waiting, Status.Queued]) && handleQueue(result);
      forState([Status.Processing]) && getWebSocket()?.close();
    }
  }, [readyState, lastMessage, handleQueue, forState, getWebSocket]);
}
