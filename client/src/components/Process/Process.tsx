import { Countdown, Progress, useCountdown } from 'components';

function Process({ data, nodes }: { data?: Data; nodes: NodeInstance[] }) {
  const progress = data?.progress ?? 0;
  const instance: NodeInstance = nodes.find((node: NodeInstance) => node.provider_name === data?.provider) ?? {
    name: '',
    provider_id: '',
    provider_name: '',
  };

  const countdown = useCountdown(data);

  return (
    <Progress width={progress}>
      <div className="mt-[1.2rem] flex flex-col text-left text-[9px]">
        {data?.provider && (
          <span className="top-[2rem] left-0 md:absolute">
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
        <Countdown {...countdown} customStyles="top-[2rem] right-[10rem] before:hidden md:absolute md:before:block" />
        <span className="top-[2rem] right-0 before:absolute before:-left-[0.7rem] before:leading-[1.2rem] md:absolute md:before:content-['|']">
          {nodes.length ?? '-'} {nodes.length === 1 ? 'node' : 'nodes'} connected
        </span>
      </div>
      <span className="absolute -top-[0.1rem] right-[0.4rem] text-[9px] text-black">{progress}%</span>
    </Progress>
  );
}

export default Process;
