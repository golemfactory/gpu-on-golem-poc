import { useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import * as Sentry from '@sentry/nextjs';
import { Status, Statuses } from 'enums/status';
import { setError } from 'slices/error';
import { selectStatus, setStatus } from 'slices/status';

export function useStatusState() {
  const status = useSelector(selectStatus);

  const forState = useCallback((statuses: Status[]) => statuses.includes(status), [status]);

  const notForState = useCallback(
    (statuses: Status[]) => Statuses.filter((status: Status) => !statuses.includes(status)).includes(status),
    [status],
  );

  return { forState, notForState };
}

export function useFetch() {
  const appDispatch = useDispatch();

  return useCallback(async (path: RequestInfo | URL, options?: RequestInit | undefined) => {
    try {
      const response = await fetch(path, options);

      if (!response.ok) Sentry.captureMessage(response.status.toString());

      if (response.status === 404) return appDispatch(setStatus(Status.Error));
      else if (response.status === 429) {
        appDispatch(setStatus(Status.Error));
        appDispatch(setError(429));
      } else return await response.json();
    } catch (e) {
      Sentry.captureException(e);
      appDispatch(setStatus(Status.Error));
    }
  }, []);
}
