import { useSelector } from 'react-redux';
import { Countdown, Progress } from 'components';
import { selectData } from 'slices/data';
import { selectNodes } from 'slices/nodes';

function Process() {
  const data = useSelector(selectData);
  const nodes = useSelector(selectNodes);
  const runningNodes = nodes.filter((node) => node.state === 'running')

  const progress = data?.progress ?? 0;
  const instance: NodeInstance = nodes.find((node: NodeInstance) => node.provider_name === data?.provider) ?? {
    name: '',
    provider_id: '',
    provider_name: '',
    state: '',
  };

  const renderShortAddress = (address?: string | null, start: number = 6, stop: number = 4) =>
    address ? address.substring(0, start) + '...' + address.substring(address.length, address.length - stop) : '';

  return (
    <Progress width={progress}>
      <div className="mt-[1.2rem] flex flex-col text-12">
        {instance.provider_id && (
          <span className="top-[2rem] left-0 md:absolute">
            Computing by: {data?.provider} (
            <a
              className="underline hover:opacity-80"
              href={`https://stats.golem.network/network/provider/${instance.provider_id}`}
              target="_blank"
              rel="noreferrer"
            >
              {renderShortAddress(instance.provider_id, 8, 6)}
            </a>
            )
          </span>
        )}
        <div className="top-[2rem] right-0 inline-flex justify-center md:absolute md:justify-end">
          <Countdown customStyles="relative before:hidden md:before:block text-12" />
          <span className="relative ml-[1.4rem] inline-flex before:absolute before:-left-[0.8rem] before:leading-[1.2rem] before:content-['|']">
            {runningNodes.length ?? '-'} {runningNodes.length === 1 ? 'node' : 'nodes'} connected
          </span>
        </div>
      </div>
      <span className="absolute -top-[0.1rem] right-[0.4rem] text-[0.9rem] text-black">{progress}%</span>
    </Progress>
  );
}

export default Process;
