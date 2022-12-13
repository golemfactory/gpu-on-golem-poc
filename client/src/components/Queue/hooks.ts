import { useCallback, useEffect, useState } from 'react';
import useWebSocket from 'react-use-websocket';
import { Api } from 'enums/api';
import { Status } from 'enums/status';
import { useStatusState } from 'utils/hooks';
import url from 'utils/url';

export function useQueue(state: State, dispatch: (action: Action) => void) {
  const { forState } = useStatusState(state);

  const [socketUrl, setSocketUrl] = useState<string | null>(null);
  const { lastMessage, readyState, getWebSocket } = useWebSocket(socketUrl);
  const [queue, setQueue] = useState({ jobs_in_queue: 0, max_queue_size: 30 });

  const handleFetch = useCallback(async () => {
    const response = await fetch(url(Api.jobsInQueue, false));

    if (response.status === 404) return dispatch({ type: Status.Error });

    return await response.json();
  }, [dispatch]);

  const handleQueue = useCallback(
    (result: { jobs_in_queue: number; max_queue_size: number }) => {
      if (result.jobs_in_queue === 0) {
        dispatch({ type: Status.Ready });
        getWebSocket()?.close();
      } else if (result.jobs_in_queue >= result.max_queue_size) {
        dispatch({ type: Status.Waiting });
      } else {
        dispatch({ type: Status.Queued });
        setQueue(result);
      }
    },
    [dispatch, getWebSocket],
  );

  useEffect(() => {
    handleFetch().then(handleQueue);

    return () => {
      getWebSocket()?.close();
    };
  }, [getWebSocket, handleFetch, handleQueue]);

  useEffect(() => {
    if (forState([Status.Waiting, Status.Queued])) {
      setSocketUrl(url(Api.jobsInQueue, true));
    }

    return () => {
      setSocketUrl(null);
    };
  }, [forState, state]);

  useEffect(() => {
    if (lastMessage) {
      const result = JSON.parse(lastMessage.data);

      handleQueue(result);
    }
  }, [readyState, lastMessage, handleQueue]);

  return queue;
}
