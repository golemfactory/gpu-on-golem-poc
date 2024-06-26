export enum Status {
  Loading = 'loading',
  Waiting = 'waiting',
  Ready = 'ready',
  Queued = 'queued',
  Processing = 'processing',
  Finished = 'finished',
  Blocked = 'blocked',
  Error = 'error',
}

export const Statuses = [
  Status.Loading,
  Status.Waiting,
  Status.Ready,
  Status.Queued,
  Status.Processing,
  Status.Finished,
  Status.Blocked,
  Status.Error,
];
