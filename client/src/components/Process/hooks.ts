import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { Api } from 'enums/api';
import { Status } from 'enums/status';
import { setError } from 'slices/error';
import { setNodes } from 'slices/nodes';
import { setStatus } from 'slices/status';
import { useFetch } from 'utils/hooks';
import url from 'utils/url';

export function useNodes() {
  const dispatch = useDispatch();

  const handleFetch = useFetch();

  useEffect(() => {
    handleFetch(url(Api.cluster, false)).then(({ cluster }: { cluster: { instances: NodeInstance[] } }) => {
      if (cluster?.instances.length === 0) {
        dispatch(setStatus(Status.Error));
        dispatch(setError(503));
      } else {
        dispatch(setNodes(cluster.instances));
      }
    });
  }, [dispatch, handleFetch]);
}
