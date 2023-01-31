import { useSelector } from 'react-redux';
import { Countdown, Facts, useCountdown } from 'components';
import { selectJobsInQueue } from 'slices/queue';

function Queue({ state }: { state: State }) {
  const jobs_in_queue = useSelector(selectJobsInQueue);

  const countdown = useCountdown();

  return (
    <>
      <div className="inline-flex text-[9px]">
        <span className="min-w-[6rem] capitalize">
          Queue {state.queue_position ?? '-'}/{jobs_in_queue}
        </span>
        <Countdown {...countdown} customStyles="relative ml-[1rem]" />
      </div>
      <Facts />
    </>
  );
}

export default Queue;
