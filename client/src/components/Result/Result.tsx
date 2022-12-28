import { useEffect, useState } from 'react';
import { Status } from 'enums/status';
import { Copy, View } from 'components';
import { useStatusState } from 'utils/hooks';
import url from 'utils/url';

function Result({ state, data, value, onReset }: { state: State; data?: Data; value: string; onReset: () => void }) {
  const { forState } = useStatusState(state);

  const [src, setSrc] = useState('');

  useEffect(() => {
    forState([Status.Processing]) && setSrc(url(data?.intermediary_images?.at(-1) ?? '', false));
    forState([Status.Finished]) && setSrc(url(data?.img_url ?? '', false));
  }, [data?.img_url, data?.intermediary_images, forState]);

  const handleOpen = () => window.open('https://chat.golem.network/');

  return (
    <div className="mt-[12rem] mb-[8rem]">
      <h2 className="text-36">Result for:</h2>
      <h3 className="my-[1.2rem] text-12 text-stone">{value}</h3>
      <Copy value={value} />
      {forState([Status.Processing]) && (
        <>
          {!!data?.intermediary_images?.at(-1) ? (
            <View src={src} value={value} />
          ) : (
            <div className="mx-auto h-[36.2rem] w-[36.2rem] bg-black" />
          )}
          <p className="mt-[5.7rem] mb-[2.4rem] text-14">
            Fun facts:
            <br />
            <br />
            Golem aims to be the first real decentralized marketplace for computing. And it seems that its doing its job
            right now, as real nodes are computing your task!
          </p>
        </>
      )}
      {forState([Status.Finished]) && (
        <>
          <View src={src} value={value} />
          <p className="mt-[5.7rem] mb-[2.4rem] text-14">
            We hope you enjoy your results! Drop us a line on our Discord chat and share your experience :)
          </p>
        </>
      )}
      <div className="mb-[1.8rem]">
        <button className="button bg-white text-black" onClick={onReset}>
          Start over
        </button>
        <button className="button" onClick={handleOpen}>
          Chat with us!
        </button>
      </div>
      <a
        className="font-sans font-light uppercase text-grey underline hover:text-white"
        href="https://handbook.golem.network/"
        target="_blank"
        rel="noreferrer"
      >
        Check our sdk
      </a>
    </div>
  );
}

export default Result;
