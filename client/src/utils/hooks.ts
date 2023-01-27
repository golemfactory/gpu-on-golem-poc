import { useCallback } from 'react';
import * as Sentry from '@sentry/nextjs';
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

        if (!response.ok) Sentry.captureMessage(response.status.toString());

        if (response.status === 404) return dispatch({ type: Status.Error });
        else if (response.status === 429) return dispatch({ type: Status.Error, error: response.status });
        else return await response.json();
      } catch (e) {
        Sentry.captureException(e);
        dispatch({ type: Status.Error });
      }
    },
    [dispatch],
  );
}
