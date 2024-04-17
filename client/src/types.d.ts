type Data = {
  eta: number | undefined;
  image: string | undefined;
  img_url: string | undefined;
  intermediary_images: string[] | undefined;
  job_id: string | undefined;
  progress: number | undefined;
  provider: string | undefined;
  socketUrl: string | null;
};

type NodeInstance = {
  name: string;
  provider_id: string;
  provider_name: string;
  state: string;
};

type Noop = () => void;
