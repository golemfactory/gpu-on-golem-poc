type State = {
  status: Status;
  job_id: string | undefined;
  error: number | undefined;
};

type Action = {
  type: Status;
  payload?: string;
  error?: number;
};

type Data = {
  eta: number;
  img_url: string;
  intermediary_images: string[];
  progress: number;
  provider: string;
};

type NodeInstance = {
  name: string;
  provider_id: string;
  provider_name: string;
};

type useReducerProps = {
  state: State;
  dispatch: (action: Action) => void;
};
