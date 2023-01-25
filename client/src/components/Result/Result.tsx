import { ReactNode, useEffect, useState } from 'react';
import { Status } from 'enums/status';
import { Copy, Placeholder, Process, View } from 'components';
import { useStatusState } from 'utils/hooks';
import url from 'utils/url';

function Result({
  state,
  data,
  value,
  onReset,
  nodes,
}: {
  state: State;
  data?: Data;
  value: string;
  onReset: () => void;
  nodes: NodeInstance[];
}) {
  const { forState } = useStatusState(state);

  const [src, setSrc] = useState('');

  useEffect(() => {
    forState([Status.Processing]) && setSrc(url(data?.intermediary_images?.at(-1) ?? '', false));
    forState([Status.Finished, Status.Blocked]) && setSrc(url(data?.img_url ?? '', false));
  }, [data?.img_url, data?.intermediary_images, forState]);

  const handleOpen = () => window.open('https://discord.com/channels/684703559954333727/849965303055384597');

  const facts = [
    'Golem aims to be the first real decentralized marketplace for computing. And it seems that its doing its job right now, as real nodes are computing your task!',
    'Did you know there are some special filters included? No funny pictures here!',
    'Third fun fact placeholder is here. How fast can you read it?',
  ];

  const [index, setIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => setIndex((state: number) => (state !== facts.length - 1 ? state + 1 : 0)), 5000);

    return () => {
      clearInterval(interval);
    };
  }, [facts.length]);

  const renderText = (children: ReactNode) => (
    <p className="mt-[5.7rem] mb-[2.4rem] min-h-[9.5rem] text-14">{children}</p>
  );

  return (
    <div className="mt-[20rem] mb-[8rem] xl:mt-[12rem]">
      <h2 className="text-24">
        Your artwork generated based <br />
        on the following keywords:
      </h2>
      <h3 className="my-[1.2rem] text-12 text-stone">{value}</h3>
      <Copy value={value} />
      {forState([Status.Processing]) && (
        <div className="mx-auto md:w-[75%]">
          {!!data?.intermediary_images?.at(-1) ? <View src={src} value={value} /> : <Placeholder />}
          <br />
          <br />
          <Process data={data} nodes={nodes} />
          {renderText(
            <span className="mt-[8rem] md:mt-0">
              Fun facts:
              <br />
              <br />
              {facts[index]}
            </span>,
          )}
        </div>
      )}
      {forState([Status.Finished]) && (
        <div className="mx-auto md:w-[75%]">
          <View src={src} value={value} />
          {renderText(
            'Want to give us feedback? Go to our Discord, find the channel GPU PoC - AI Image Generator and get involved!',
          )}
        </div>
      )}
      {forState([Status.Blocked]) && (
        <div className="mx-auto md:w-[75%]">
          <View src={src} value={value} blocked />
          {renderText('Sorry, this image violates our NSFW filters :(')}
        </div>
      )}
      <div className="mb-[1.8rem] flex justify-center">
        <button className="button mx-[0.5rem] bg-white text-black md:mx-[1.8rem]" onClick={onReset}>
          Start over
        </button>
        <button className="button mx-[0.5rem] md:mx-[1.8rem]" onClick={handleOpen}>
          Go to Discord
        </button>
      </div>
    </div>
  );
}

export default Result;
