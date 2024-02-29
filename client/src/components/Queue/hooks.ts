import { useCallback, useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useEffectOnce } from 'react-use';
import useWebSocket from 'react-use-websocket';
import { Api } from 'enums/api';
import { Status } from 'enums/status';
import { selectJobId } from 'slices/data';
import { setQueue } from 'slices/queue';
import { setStatus } from 'slices/status';
import { useStatusState } from 'utils/hooks';
import url from 'utils/url';

export function useQueue() {
  const dispatch = useDispatch();
  const job_id = useSelector(selectJobId);

  const { forState } = useStatusState();

  const [socketUrl, setSocketUrl] = useState<string | null>(null);
  const { lastMessage, readyState, getWebSocket } = useWebSocket(socketUrl);

  const handleQueue = useCallback(
    (result: { jobs_in_queue: number; hold_off_user: boolean }) => {
      const { hold_off_user, ...args } = result;

      if (hold_off_user) return dispatch(setStatus(Status.Waiting));

      if (result?.jobs_in_queue === 0) {
        forState([Status.Loading, Status.Ready]) && dispatch(setStatus(Status.Ready));
        forState([Status.Loading, Status.Ready]) && !job_id && dispatch(setQueue(args));
      } else {
        forState([Status.Loading, Status.Ready]) && dispatch(setStatus(!!job_id ? Status.Queued : Status.Ready));
      }
    },
    [dispatch, forState, job_id],
  );

  useEffectOnce(() => {
    setSocketUrl(url(Api.jobsInQueue, true));
  });

  useEffect(() => {
    if (lastMessage) {
      const result = JSON.parse(lastMessage.data);

      forState([Status.Loading, Status.Waiting, Status.Queued]) && handleQueue(result);
      forState([Status.Processing]) && getWebSocket()?.close();
    }
  }, [readyState, lastMessage, handleQueue, forState, getWebSocket]);
}
