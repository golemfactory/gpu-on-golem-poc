import ReactCountdown, { CountdownRenderProps } from 'react-countdown';

function Locked({ until, onUpdate }: { until: number | null; onUpdate: (value: number | null) => void }) {
  return (
    <ReactCountdown
      date={!!until ? new Date(until) : undefined}
      intervalDelay={0}
      precision={0}
      renderer={renderer}
      onComplete={() => onUpdate(null)}
    />
  );
}

function renderer(args: CountdownRenderProps) {
  const { completed, minutes, seconds } = args;

  const timeLeft = `${minutes.toString().padStart(2, '0')}m ${seconds.toString().padStart(2, '0')}s`;

  return !completed ? (
    <div className="inline-flex font-normal text-blue">
      <span className="mr-4 uppercase">Next use:</span> {completed ? '--.-' : timeLeft} left
    </div>
  ) : null;
}

export default Locked;
