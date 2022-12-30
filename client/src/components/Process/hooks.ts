import { useEffect, useState } from 'react';
import { Api } from 'enums/api';
import { Status } from 'enums/status';
import { useFetch, useStatusState } from 'utils/hooks';
import url from 'utils/url';

export function useNodes({ state, dispatch }: useReducerProps) {
  const { forState } = useStatusState(state);

  const [nodes, setNodes] = useState<NodeInstance[]>([]);

  const handleFetch = useFetch(dispatch);

  useEffect(() => {
    if (forState([Status.Processing]) && state.job_id) {
      handleFetch(url(Api.cluster, false)).then(({ cluster }: { cluster: { instances: NodeInstance[] } }) =>
        setNodes(cluster.instances),
      );
    }
  }, [forState, handleFetch, state.job_id]);

  return nodes;
}
