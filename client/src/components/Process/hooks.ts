import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { Api } from 'enums/api';
import { Status } from 'enums/status';
import { setNodes } from 'slices/nodes';
import { setError } from 'slices/error';
import { setStatus } from 'slices/status';
import { useFetch } from 'utils/hooks';
import url from 'utils/url';

export function useNodes() {
  const appDispatch = useDispatch();

  const handleFetch = useFetch();

  useEffect(() => {
    handleFetch(url(Api.cluster, false)).then(({ cluster }: { cluster: { instances: NodeInstance[] } }) => {
      if (cluster?.instances.length === 0) {
        appDispatch(setStatus(Status.Error));
        appDispatch(setError(503));
      } else {
        appDispatch(setNodes(cluster.instances));
      }
    });
  }, []);
}
