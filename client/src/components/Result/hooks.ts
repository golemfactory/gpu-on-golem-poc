import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import useWebSocket from 'react-use-websocket';
import { Api } from 'enums/api';
import { Status } from 'enums/status';
import { resetData, selectJobId, setData } from 'slices/data';
import { setQueue } from 'slices/queue';
import { setStatus } from 'slices/status';
import { useStatusState } from 'utils/hooks';
import url from 'utils/url';

export function useResult() {
  const dispatch = useDispatch();
  const job_id = useSelector(selectJobId);

  const { forState } = useStatusState();

  const [socketUrl, setSocketUrl] = useState<string | null>(null);
  const { lastMessage, readyState, getWebSocket } = useWebSocket(socketUrl);

  useEffect(() => {
    !!job_id && setSocketUrl(url(Api.txt2img, true, job_id));
  }, [job_id]);

  useEffect(() => {
    if (lastMessage) {
      const { status, jobs_in_queue, queue_position, ...data } = JSON.parse(lastMessage.data);

      if (forState([Status.Queued, Status.Processing])) {
        dispatch(setData(data));
        dispatch(setStatus(status));
        !!job_id && dispatch(setQueue({ jobs_in_queue, queue_position }));
      } else if (forState([Status.Finished])) {
        getWebSocket()?.close();
      }
    }
  }, [readyState, lastMessage, job_id, forState, getWebSocket]);

  const handleReset = () => {
    dispatch(resetData());
    setSocketUrl(null);
  };

  return { onReset: handleReset };
}
