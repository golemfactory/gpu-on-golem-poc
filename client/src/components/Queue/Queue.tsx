import { Countdown, Facts, useCountdown } from 'components';

function Queue({ jobs_in_queue, state, data }: { jobs_in_queue: number; state: State; data?: Data }) {
  const countdown = useCountdown(data);

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
