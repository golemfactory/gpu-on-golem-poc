type State = {
  job_id: string | undefined;
  error: number | undefined;
};

type Action = {
  payload?: {
    job_id?: string;
  };
  error?: number;
};

type Data = {
  eta: number | undefined;
  img_url: string | undefined;
  intermediary_images: string[] | undefined;
  progress: number | undefined;
  provider: string | undefined;
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
