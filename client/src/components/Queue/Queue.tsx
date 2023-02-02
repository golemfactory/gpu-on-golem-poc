import { useSelector } from 'react-redux';
import { Countdown } from 'components';
import { selectQueuePosition } from 'slices/queue';

function Queue() {
  const queue_position = useSelector(selectQueuePosition);

  return queue_position > 0 ? (
    <>
      <div className="flex flex-col text-[9px] md:flex-row">
        <div className="flex min-w-[6rem] flex-col text-left md:flex-row">
          <span className="md:mr-[0.4rem]">Your request has been accepted and is awaiting processing.</span>
          <span>You are number {queue_position ?? '-'} in the queue.</span>
        </div>
        <Countdown customStyles="relative md:ml-[1rem] before:hidden md:before:block" />
      </div>
    </>
  ) : null;
}

export default Queue;
