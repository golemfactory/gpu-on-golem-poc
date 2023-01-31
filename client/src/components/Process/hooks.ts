import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { Api } from 'enums/api';
import { Status } from 'enums/status';
import { setNodes } from 'slices/nodes';
import { useFetch } from 'utils/hooks';
import url from 'utils/url';

export function useNodes({ state, dispatch }: useReducerProps) {
  const appDispatch = useDispatch();

  const handleFetch = useFetch(dispatch);

  useEffect(() => {
    handleFetch(url(Api.cluster, false)).then(({ cluster }: { cluster: { instances: NodeInstance[] } }) => {
      if (cluster?.instances.length === 0) return dispatch({ type: Status.Error, error: 503 });
      else {
        appDispatch(setNodes(cluster.instances));
        dispatch({
          type: state.status,
          payload: {
            job_id: state.job_id,
            queue_position: state.queue_position,
          },
        });
      }
    });
  }, []);
}
