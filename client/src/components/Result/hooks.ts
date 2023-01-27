import { useEffect, useState } from 'react';
import useWebSocket from 'react-use-websocket';
import { Api } from 'enums/api';
import { Status } from 'enums/status';
import { useStatusState } from 'utils/hooks';
import url from 'utils/url';

export function useResult({ state, dispatch }: useReducerProps) {
  const { forState } = useStatusState(state);

  const [socketUrl, setSocketUrl] = useState<string | null>(null);
  const { lastMessage, readyState, getWebSocket } = useWebSocket(socketUrl);
  const [data, setData] = useState<Data | undefined>(undefined);

  useEffect(() => {
    if (state.job_id) {
      setSocketUrl(url(Api.txt2img, true, state.job_id));
    }
  }, [state.job_id]);

  useEffect(() => {
    if (lastMessage) {
      const { status, queue_position, ...data } = JSON.parse(lastMessage.data);

      if (forState([Status.Queued, Status.Processing])) {
        setData(data);
        dispatch({ type: status, payload: { job_id: state.job_id, queue_position } });
      } else if (forState([Status.Finished])) {
        getWebSocket()?.close();
      }
    }
  }, [readyState, lastMessage, dispatch, state.job_id, forState, getWebSocket]);

  const handleReset = () => {
    setData(undefined);
    setSocketUrl(null);
  };

  return { data, onReset: handleReset };
}
