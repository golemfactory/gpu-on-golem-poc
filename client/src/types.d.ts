type State = {
  job_id: string | undefined;
  queue_position: number | undefined;
  error: number | undefined;
};

type Action = {
  payload?: {
    job_id?: string;
    queue_position?: number;
  };
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
