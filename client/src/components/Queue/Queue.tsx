import { useEffect, useState } from 'react';
import { Progress } from 'components';

function Queue({ jobs_in_queue, queue_position }: { jobs_in_queue: number; queue_position?: number }) {
  const [percent, setPercent] = useState(0);

  useEffect(() => {
    setPercent(Math.floor(((queue_position ?? 100) * 100) / jobs_in_queue));

    return () => {
      setPercent(0);
    };
  }, [jobs_in_queue, queue_position]);

  return (
    <>
      <Progress width={percent}>
        <span className="absolute top-[2rem] left-0 text-[9px] capitalize">
          Queue {queue_position ?? '-'}/{jobs_in_queue}
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
