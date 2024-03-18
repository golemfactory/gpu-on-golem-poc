import { useSelector } from 'react-redux';
import { Countdown, Progress } from 'components';
import { selectData } from 'slices/data';
import { selectNodes } from 'slices/nodes';

function Process() {
  const data = useSelector(selectData);
  const nodes = useSelector(selectNodes);

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
    <>
      <div className="my-[1.6rem] bg-white p-[24px]">
        <Progress width={progress}>
          <div className="text-[14px]">
            <span className="absolute top-[14px] left-[8px] hidden md:block">Generating image...</span>
            <span className="absolute left-[8px] top-[14px] md:left-1/2">{progress}%</span>
            <div className="absolute top-[14px] right-[8px] inline-flex justify-center md:justify-end">
              <Countdown />
            </div>
          </div>
        </Progress>
      </div>
      {instance.provider_id && (
        <span className="text-[14px] font-light">
          Computing by: {data?.provider} (
          <a
            className="underline"
            href={`https://stats.golem.network/network/provider/${instance.provider_id}`}
            target="_blank"
            rel="noreferrer"
          >
            {renderShortAddress(instance.provider_id, 8, 6)}
          </a>
          )
        </span>
      )}
    </>
  );
}

export default Process;
