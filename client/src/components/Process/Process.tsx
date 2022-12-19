import { Status } from 'enums/status';
import { Progress } from 'components';

function Process({ status, data }: { status: Status; data?: Data }) {
  const progress = data?.progress ?? 0;

  return (
    <Progress width={progress}>
      <span className="absolute top-[2rem] left-0 capitalize">{status}</span>
      <span className="absolute top-[2rem] right-0">{progress}%</span>
    </Progress>
  );
}

export default Process;
