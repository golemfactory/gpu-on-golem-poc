import { useEffect, useState } from 'react';
import useWebSocket from 'react-use-websocket';
import { Api } from 'enums/api';
import { Status } from 'enums/status';
import url from 'utils/url';

export function useQueue(state: State, dispatch: (action: Action) => void) {
  const [socketUrl, setSocketUrl] = useState<string | null>(null);
  const { lastMessage, readyState } = useWebSocket(socketUrl);
  const [queue, setQueue] = useState({ jobs_in_queue: 0, max_queue_size: 30 });

  const handleFetch = async () => {
    const response = await fetch(url(Api.jobsInQueue, false));

    if (response.status === 404) return dispatch({ type: Status.Error });

    return await response.json();
  };

  const handleQueue = (result: { jobs_in_queue: number; max_queue_size: number }) => {
    if (result.jobs_in_queue === 0) {
      dispatch({ type: Status.Ready });
    } else if (result.jobs_in_queue >= result.max_queue_size) {
      dispatch({ type: Status.Waiting });
    } else {
      dispatch({ type: Status.Queued });
      setQueue(result);
    }
  };

  useEffect(() => {
    handleFetch().then(handleQueue);
  }, []);

  useEffect(() => {
    if ([Status.Waiting, Status.Queued].includes(state.status)) {
      setSocketUrl(url(Api.jobsInQueue, true));
    }
  }, [state]);

  useEffect(() => {
    if (lastMessage) {
      const result = JSON.parse(lastMessage.data);

      handleQueue(result);
    }
  }, [readyState, lastMessage]);

  return queue;
}
