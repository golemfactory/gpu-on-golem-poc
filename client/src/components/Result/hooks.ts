import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import useWebSocket from 'react-use-websocket';
import { Api } from 'enums/api';
import { Status } from 'enums/status';
import {
  selectData,
  selectEta,
  selectJobId,
  selectSocketUrl,
  setData,
  setEta,
  setJobId,
  setProvider,
  setSocketUrl,
} from 'slices/data';
import { selectQueue, setQueue } from 'slices/queue';
import { selectStatus, setStatus } from 'slices/status';
import { useStatusState } from 'utils/hooks';
import url from 'utils/url';

export function useResult() {
  const dispatch = useDispatch();
  const socketUrl = useSelector(selectSocketUrl);
  const job_id = useSelector(selectJobId);
  const data = useSelector(selectData);
  const eta = useSelector(selectEta);
  const queue = useSelector(selectQueue);
  const status = useSelector(selectStatus);

  const { forState } = useStatusState();

  const { lastMessage, readyState, getWebSocket } = useWebSocket(socketUrl);

  useEffect(() => {
    !!job_id && dispatch(setSocketUrl(url(Api.txt2img, true, job_id)));
  }, [job_id]);

  useEffect(() => {
    if (lastMessage) {
      const { jobs_in_queue, queue_position, ...result } = JSON.parse(lastMessage.data);

      if (forState([Status.Queued, Status.Processing])) {
        !job_id && dispatch(setJobId(result.job_id));
        !data.provider && dispatch(setProvider(result.provider));
        !eta && dispatch(setEta(result.eta));

        if (result.status !== status) {
          dispatch(setStatus(result.status));
          dispatch(setEta(result.eta));
        }

        if (!!job_id && (queue.jobs_in_queue !== jobs_in_queue || queue.queue_position !== queue_position)) {
          dispatch(setQueue({ jobs_in_queue, queue_position }));
        }

        dispatch(
          setData({
            img_url: result.img_url,
            intermediary_images: result.intermediary_images,
            progress: result.progress,
          }),
        );
      } else if (forState([Status.Finished])) {
        getWebSocket()?.close();
      }
    }
  }, [dispatch, readyState, lastMessage, data.provider, job_id, status, queue, forState, getWebSocket]);
}
