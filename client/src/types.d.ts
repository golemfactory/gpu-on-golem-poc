type State = {
  status: Status;
  job_id: string | undefined;
};

type Action = {
  type: Status;
  payload?: string;
};

type Data = {
  progress: number;
  img_url: string;
};
