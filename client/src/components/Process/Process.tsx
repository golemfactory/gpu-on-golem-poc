import { useEffect, useState } from 'react';
import { Status } from 'enums/status';
import { Progress } from 'components';

function Process({ status, progress }: { status: Status; progress?: number }) {
  const [percent, setPercent] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => setPercent((state: number) => (state === 100 ? state : state + 1)), 500);

    return () => {
      clearInterval(interval);
    };
  }, []);

  return (
    <Progress width={progress ?? percent}>
      <span className="absolute top-[2rem] left-0 capitalize">{status}</span>
      <span className="absolute top-[2rem] right-0">{progress ?? percent}%</span>
    </Progress>
  );
}

export default Process;
