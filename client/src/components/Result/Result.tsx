import { ReactNode } from 'react';
import { useSelector } from 'react-redux';
import { Status } from 'enums/status';
import { Copy, Facts, Placeholder, Process, View } from 'components';
import { selectData } from 'slices/data';
import { useStatusState } from 'utils/hooks';

function Result({ value, onReset }: { value: string; onReset: () => void }) {
  const data = useSelector(selectData);

  const { forState } = useStatusState();

  const [intermediary_image] = data?.intermediary_images ? data?.intermediary_images.slice(-1) : [];

  const handleOpen = () => window.open('https://discord.com/channels/684703559954333727/849965303055384597');

  const renderText = (children: ReactNode) => (
    <p className="mt-[3.6rem] -mb-[3.2rem] min-h-[9.5rem] text-14">{children}</p>
  );

  return (
    <div className="mt-[18rem] mb-[2.4rem] md:mb-0 xl:mt-[12rem]">
      <h2 className="text-24">Your artwork based on the following keywords:</h2>
      <div className="relative mx-auto pr-[2rem] md:max-w-[50%] md:pr-0">
        <h3 className="mt-[1.2rem] mb-[2.8rem] text-12 text-stone">{value}</h3>
        <Copy value={value} />
      </div>
      {forState([Status.Processing]) && (
        <div className="mx-auto md:w-[75%]">
          {!!intermediary_image ? <View intermediary_image={intermediary_image} value={value} /> : <Placeholder />}
          <br />
          <br />
          <Process />
          <Facts />
        </div>
      )}
      {forState([Status.Finished]) && (
        <div className="mx-auto md:w-[75%]">
          <View value={value} />
          {renderText(
            'Want to give us feedback? Go to our Discord, find the channel GPU PoC - AI Image Generator and get involved!',
          )}
        </div>
      )}
      {forState([Status.Blocked]) && (
        <div className="mx-auto md:w-[75%]">
          <View value={value} blocked />
          {renderText('Sorry, this image violates our NSFW filters :(')}
        </div>
      )}
      {forState([Status.Finished, Status.Blocked]) && (
        <div className="mb-[1.8rem] flex justify-center">
          <button className="button mx-[0.5rem] bg-white text-black md:mx-[1.8rem]" onClick={onReset}>
            Start over
          </button>
          <button className="button mx-[0.5rem] md:mx-[1.8rem]" onClick={handleOpen}>
            Go to Discord
          </button>
        </div>
      )}
    </div>
  );
}

export default Result;
