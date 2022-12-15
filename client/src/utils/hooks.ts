import { useCallback } from 'react';
import { Status, Statuses } from 'enums/status';

export function useStatusState(state: State) {
  const forState = useCallback((statuses: Status[]) => statuses.includes(state.status), [state.status]);

  const notForState = useCallback(
    (statuses: Status[]) => Statuses.filter((status: Status) => !statuses.includes(status)).includes(state.status),
    [state.status],
  );

  return { forState, notForState };
}

export function useFetch(dispatch: (action: Action) => void) {
  return useCallback(
    async (path: RequestInfo | URL, options?: RequestInit | undefined) => {
      try {
        const response = await fetch(path, options);

        if (response.status === 404) return dispatch({ type: Status.Error });

        return await response.json();
      } catch (e) {
        dispatch({ type: Status.Error });
      }
    },
    [dispatch],
  );
}
