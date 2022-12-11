import Image from 'next/image';
import { saveAs } from 'file-saver';
import url from 'utils/url';

function Result({ data, value, onReset }: { data?: Data; value: string; onReset: () => void }) {
  const src = url(data?.img_url ?? '', false);

  const handleSave = () => saveAs(src, `${value}.png`);

  const handleOpen = () => window.open('https://chat.golem.network/');

  return (
    <div className="mt-[5rem] mb-[8rem]">
      <h2 className="text-36">Result for:</h2>
      <h3 className="mt-[1.2rem] mb-[2.4rem] text-12 text-[#9c9c9c]">{value}</h3>
      <div className="relative mx-auto w-[36.2rem]">
        <Image className="mx-auto" src={src} alt={value} width={362} height={362} />
        <button
          className="absolute bottom-[1rem] right-[1rem] h-[2rem] w-[1.8rem] bg-black bg-[url('/download.svg')] bg-center bg-no-repeat"
          onClick={handleSave}
        />
      </div>
      <p className="mt-[5.7rem] mb-[2.4rem] text-14">
        We hope you enjoy your results! Drop us a line on our Discord chat and share your experience :)
      </p>
      <div className="mb-[1.8rem]">
        <button className="button bg-white text-black" onClick={onReset}>
          Start over
        </button>
        <button className="button" onClick={handleOpen}>
          Chat with us!
        </button>
      </div>
      <a
        className="font-sans font-light uppercase text-grey underline"
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
