import { Countdown, useCountdown } from 'components';

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
      <p className="mt-[5.7rem] mb-[2.4rem] text-14">Fun facts:</p>
      <p className="text-18">
        You are now waiting in the queue for your turn. There are 2 turns. Right and left. We have to hire a new
        copywriter… you know anyone?
      </p>
    </>
  );
}

export default Queue;
