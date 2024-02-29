import { ReactNode } from 'react';
import { useSelector } from 'react-redux';
import Image from 'next/image';
import { Status } from 'enums/status';
import { renderIcon } from 'assets/utils';
import { Copy, Process, View } from 'components';
import { selectData } from 'slices/data';
import { useStatusState } from 'utils/hooks';

function Result({ value, onReset }: { value: string; onReset: Noop }) {
  const data = useSelector(selectData);

  const { forState } = useStatusState();

  const [intermediary_image] = data?.intermediary_images ? data?.intermediary_images.slice(-1) : [];

  const handleOpen = () => window.open('https://discord.com/channels/684703559954333727/1072529851346595840');

  const renderText = (children: ReactNode) => <p className="mt-[1.6rem] text-14 font-light">{children}</p>;

  return (
    <div className="mt-[12rem] mb-[2.4rem] md:mb-0 xl:mt-[12rem]">
      <div className="relative mx-auto mb-[1.6rem] flex gap-4 bg-white p-3 pr-10 md:w-[75%]">
        <h3 className="mx-auto flex flex-col text-12 uppercase md:flex-row">
          Your prompt:<span className="ml-2 w-[300px] truncate text-blue md:w-[400px]">{value}</span>
        </h3>
        <Copy value={value} />
      </div>
      {forState([Status.Processing]) && (
        <div className="mx-auto md:w-[75%]">
          <View intermediary_image={intermediary_image} value={value} />
          <Process />
        </div>
      )}
      {forState([Status.Finished]) && (
        <div className="mx-auto md:w-[75%]">
          <View value={value} onReset={onReset} />
          {renderText(
            'Want to give us feedback? Go to our Discord, find the channel "image-generator-discussion" and get involved!',
          )}
        </div>
      )}
      {forState([Status.Blocked]) && (
        <div className="mx-auto md:w-[75%]">
          <View value={value} onReset={onReset} blocked />
          {renderText('Sorry, this image violates our NSFW filters.')}
        </div>
      )}
      {forState([Status.Finished, Status.Blocked]) && (
        <button
          className="min-w-10 mx-auto mt-[2.4rem] flex border-[#5865F2] bg-[#5865F2] p-[12px] text-[12px] tracking-[2px] hover:border-[#5865F2] hover:bg-[#5865F2] hover:text-white"
          onClick={handleOpen}
        >
          <Image className="mr-4" src={renderIcon('discordWhite')} alt="discord logo" width={18} height={18} />
          Join Discord
        </button>
      )}
    </div>
  );
}

export default Result;
