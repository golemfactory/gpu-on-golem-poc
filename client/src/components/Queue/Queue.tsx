import { useSelector } from 'react-redux';
import { Countdown } from 'components';
import { selectQueuePosition } from 'slices/queue';

function Queue() {
  const queue_position = useSelector(selectQueuePosition);

  const renderText = () =>
    `There ${queue_position > 1 ? 'are' : 'is'} ${queue_position ?? '-'} request${
      queue_position > 1 ? 's' : ''
    } ahead of you.`;

  return queue_position > 0 ? (
    <div className="mx-auto w-[75%] md:mt-[5.7rem]">
      <span className="mr-[0.4rem] text-12">Your request has been accepted and is awaiting processing.</span>
      <div>
        <span className="mr-[0.4rem] text-12">{renderText()}</span>
        <Countdown customStyles="relative before:hidden text-12" />
      </div>
    </div>
  ) : null;
}

export default Queue;
