import { Status, Statuses } from 'enums/status';

export function useStatusState(state: State) {
  const forState = (statuses: Status[]) => statuses.includes(state.status);

  const notForState = (statuses: Status[]) =>
    Statuses.filter((status: Status) => !statuses.includes(status)).includes(state.status);

  return { forState, notForState };
}
