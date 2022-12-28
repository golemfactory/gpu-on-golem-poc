type State = {
  status: Status;
  job_id: string | undefined;
};

type Action = {
  type: Status;
  payload?: string;
};

type Data = {
  img_url: string;
  intermediary_images: string[];
  progress: number;
};
