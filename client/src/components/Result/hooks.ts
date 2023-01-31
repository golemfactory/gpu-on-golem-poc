import { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import useWebSocket from 'react-use-websocket';
import { Api } from 'enums/api';
import { Status } from 'enums/status';
import { resetData, setData } from 'slices/data';
import { setQueue } from 'slices/queue';
import { setStatus } from 'slices/status';
import { useStatusState } from 'utils/hooks';
import url from 'utils/url';

export function useResult({ state, dispatch }: useReducerProps) {
  const appDispatch = useDispatch();

  const { forState } = useStatusState();

  const [socketUrl, setSocketUrl] = useState<string | null>(null);
  const { lastMessage, readyState, getWebSocket } = useWebSocket(socketUrl);

  useEffect(() => {
    if (state.job_id) {
      setSocketUrl(url(Api.txt2img, true, state.job_id));
    }
  }, [state.job_id]);

  useEffect(() => {
    if (lastMessage) {
      const { status, jobs_in_queue, queue_position, ...data } = JSON.parse(lastMessage.data);

      if (forState([Status.Queued, Status.Processing])) {
        appDispatch(setData(data));
        appDispatch(setStatus(status));
        dispatch({ payload: { job_id: state.job_id, queue_position } });
        !!state.job_id && appDispatch(setQueue({ jobs_in_queue }));
      } else if (forState([Status.Finished])) {
        getWebSocket()?.close();
      }
    }
  }, [readyState, lastMessage, dispatch, state.job_id, forState, getWebSocket]);

  const handleReset = () => {
    appDispatch(resetData());
    setSocketUrl(null);
  };

  return { onReset: handleReset };
}
