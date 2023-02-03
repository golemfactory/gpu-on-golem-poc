import ReactCountdown, { CountdownRenderProps } from 'react-countdown';
import { useEffect, useRef } from 'react';
import { useSelector } from 'react-redux';
import { selectEta } from 'slices/data';

function Countdown({ customStyles }: { customStyles: string }) {
  const eta = useSelector(selectEta);

  const sharedStyles =
    'inline-flex min-w-[4.5rem] text-right ' +
    "before:absolute before:-left-[1rem] before:leading-[1.2rem] before:content-['|'] ";
  const props = { className: sharedStyles + customStyles };

  const date = useRef<number>();

  useEffect(() => {
    if (eta) {
      date.current = Date.now() + eta * 1000;
    }
  }, []);

  return !!date.current ? (
    <ReactCountdown date={date.current} intervalDelay={0} precision={2} renderer={(args) => renderer(args, props)} />
  ) : (
    <div {...props}>ETA --.-</div>
  );
}

export default Countdown;

function renderer(args: CountdownRenderProps, props: { className: string }) {
  const { completed, hours, minutes, seconds, milliseconds } = args;

  const time = hours * 3600 + minutes * 60 + seconds;
  const ms = milliseconds.toString().slice(0, -2);

  return (
    <div {...props}>
      ETA {completed ? '--.-' : (time < 10 ? '0' + time : time.toString()) + '.' + (milliseconds < 100 ? '0' + ms : ms)}
    </div>
  );
}
