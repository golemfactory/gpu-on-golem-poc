import { useSelector } from 'react-redux';
import { Countdown } from 'components';
import { selectQueuePosition } from 'slices/queue';

function Queue() {
  const queue_position = useSelector(selectQueuePosition);

  return (
    <>
      <div className="inline-flex text-[9px]">
        <span className="min-w-[6rem]">
          Your request has been accepted and is awaiting processing. You are number {queue_position ?? '-'} in the
          queue.
        </span>
        <Countdown customStyles="relative ml-[1rem]" />
      </div>
    </>
  );
}

export default Queue;
