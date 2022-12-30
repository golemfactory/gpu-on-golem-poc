import { Progress } from 'components';

function Process({ data, nodes }: { data?: Data; nodes: NodeInstance[] }) {
  const progress = data?.progress ?? 0;
  const instance: NodeInstance = nodes.find((node: NodeInstance) => node.provider_name === data?.provider) ?? {
    name: '',
    provider_id: '',
    provider_name: '',
  };

  return (
    <Progress width={progress}>
      {data?.provider && (
        <span className="absolute top-[2rem] left-0 text-[9px]">
          Computing by: {data?.provider} (
          <a
            className="underline hover:opacity-80"
            href={`https://stats.golem.network/network/provider/${instance.provider_id}`}
            target="_blank"
            rel="noreferrer"
          >
            {instance.provider_id}
          </a>
          )
        </span>
      )}
      <span className="absolute top-[2rem] right-0 text-[9px]">| {nodes.length ?? '-'} nodes in the network</span>
      <span className="absolute -top-[0.1rem] right-[0.4rem] text-[9px] text-black">{progress}%</span>
    </Progress>
  );
}

export default Process;
