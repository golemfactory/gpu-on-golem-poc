import { useEffect, useState } from 'react';
import useWebSocket from 'react-use-websocket';
import { Api } from 'enums/api';
import url from 'utils/url';

export function useResult(state: State, dispatch: (action: Action) => void) {
  const [socketUrl, setSocketUrl] = useState<string | null>(null);
  const { lastMessage, readyState } = useWebSocket(socketUrl);
  const [data, setData] = useState<Data | undefined>(undefined);

  useEffect(() => {
    if (state.job_id) {
      setSocketUrl(url(Api.txt2img, true, state.job_id));
    }
  }, [state]);

  useEffect(() => {
    if (lastMessage) {
      const { status, ...data } = JSON.parse(lastMessage.data);

      setData(data);
      dispatch({ type: status });
    }
  }, [readyState, lastMessage]);

  return { data };
}
