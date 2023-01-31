import { useSelector } from 'react-redux';
import { Countdown, Facts, useCountdown } from 'components';
import { selectJobsInQueue, selectQueuePosition } from 'slices/queue';

function Queue() {
  const jobs_in_queue = useSelector(selectJobsInQueue);
  const queue_position = useSelector(selectQueuePosition);

  const countdown = useCountdown();

  return (
    <>
      <div className="inline-flex text-[9px]">
        <span className="min-w-[6rem] capitalize">
          Queue {queue_position ?? '-'}/{jobs_in_queue}
        </span>
        <Countdown {...countdown} customStyles="relative ml-[1rem]" />
      </div>
      <Facts />
    </>
  );
}

export default Queue;
