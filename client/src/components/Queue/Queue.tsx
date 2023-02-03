import { useSelector } from 'react-redux';
import { Countdown } from 'components';
import { selectQueuePosition } from 'slices/queue';

function Queue() {
  const queue_position = useSelector(selectQueuePosition);

  return queue_position > 0 ? (
    <div className="min-w-[6rem] md:mt-[5.7rem] md:text-12">
      <span className="mr-[0.4rem]">Your request has been accepted and is awaiting processing.</span>
      <div>
        <span className="mr-[0.4rem]">There are {queue_position ?? '-'} requests ahead of you. </span>
        <Countdown customStyles="relative before:hidden" />
      </div>
    </div>
  ) : null;
}

export default Queue;
