import { useEffect, useRef } from 'react';
import Countdown from 'react-countdown';
import { Progress } from 'components';

function Process({ data, nodes }: { data?: Data; nodes: NodeInstance[] }) {
  const progress = data?.progress ?? 0;
  const instance: NodeInstance = nodes.find((node: NodeInstance) => node.provider_name === data?.provider) ?? {
    name: '',
    provider_id: '',
    provider_name: '',
  };
  const countdown = useRef<number>();

  useEffect(() => {
    if (data?.progress === 0) {
      countdown.current = Date.now() + data?.eta * 1000;
    }
  }, [data?.eta, data?.progress]);

  const renderMs = (milliseconds: number) => milliseconds.toString().slice(0, -2);

  const renderer = ({
    completed,
    seconds,
    milliseconds,
  }: {
    completed: boolean;
    seconds: number;
    milliseconds: number;
  }) => (
    <div className="top-[2rem] right-[10rem] inline-flex min-w-[4.5rem] text-right before:absolute before:-left-[0.7rem] before:leading-[1.2rem] md:absolute md:before:content-['|']">
      ETA{' '}
      {completed
        ? '--.-'
        : (seconds < 10 ? '0' + seconds : seconds.toString()) +
          '.' +
          (milliseconds < 100 ? '0' + renderMs(milliseconds) : renderMs(milliseconds))}
    </div>
  );

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
        {!!countdown.current && (
          <Countdown date={countdown.current} intervalDelay={0} precision={2} renderer={renderer} />
        )}
        <span className="top-[2rem] right-0 before:absolute before:-left-[0.7rem] before:leading-[1.2rem] md:absolute md:before:content-['|']">
          {nodes.length ?? '-'} {nodes.length === 1 ? 'node' : 'nodes'} connected
        </span>
      </div>
      <span className="absolute -top-[0.1rem] right-[0.4rem] text-[9px] text-black">{progress}%</span>
    </Progress>
  );
}

export default Process;
