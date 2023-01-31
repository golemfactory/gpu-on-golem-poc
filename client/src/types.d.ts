type Data = {
  eta: number | undefined;
  img_url: string | undefined;
  intermediary_images: string[] | undefined;
  job_id: string | undefined;
  progress: number | undefined;
  provider: string | undefined;
};

type NodeInstance = {
  name: string;
  provider_id: string;
  provider_name: string;
};
