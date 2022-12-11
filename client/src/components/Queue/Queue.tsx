import { useEffect, useState } from 'react';
import { Progress } from 'components';

function Queue({ jobs_in_queue, max_queue_size }: { jobs_in_queue: number; max_queue_size: number }) {
  const [percent, setPercent] = useState(10);

  useEffect(() => {
    setPercent(Math.floor((jobs_in_queue * 100) / max_queue_size));
  }, [jobs_in_queue]);

  return (
    <>
      <Progress width={percent}>
        <span className="absolute top-[2rem] left-0 capitalize">
          Queue {jobs_in_queue}/{max_queue_size}
        </span>
      </Progress>
      <p className="mt-[5.7rem] mb-[2.4rem] text-14">Fun facts:</p>
      <p className="text-18">
        You are now waiting in the queue for your turn. There are 2 turns. Right and left. We have to hire a new
        copywriter… you know anyone?
      </p>
    </>
  );
}

export default Queue;
