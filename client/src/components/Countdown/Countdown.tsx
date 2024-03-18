import { useRef } from 'react';
import ReactCountdown, { CountdownRenderProps } from 'react-countdown';
import { useSelector } from 'react-redux';
import { useEffectOnce } from 'react-use';
import { selectEta } from 'slices/data';

function Countdown() {
  const eta = useSelector(selectEta);

  const date = useRef<number>();

  useEffectOnce(() => {
    if (eta) {
      date.current = Date.now() + eta * 1000;
    }
  });

  return !!date.current ? (
    <ReactCountdown date={date.current} intervalDelay={0} precision={2} renderer={renderer} />
  ) : null;
}

export default Countdown;

function renderer(args: CountdownRenderProps) {
  const { completed, hours, minutes, seconds, milliseconds } = args;

  const time = hours * 3600 + minutes * 60 + seconds;
  const ms = milliseconds.toString().slice(0, -2);

  return (
    <div className="relative inline-flex min-w-[4.5rem] text-right text-blue">
      {completed ? '--.-' : (time < 10 ? '0' + time : time.toString()) + '.' + (milliseconds < 100 ? '0' + ms : ms)}{' '}
      seconds left
    </div>
  );
}
