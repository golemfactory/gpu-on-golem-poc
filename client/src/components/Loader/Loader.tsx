import { useEffect, useState } from 'react';
import { Status } from 'enums/status';

function Loader({ state }: { state: State }) {
  const [timer, setTimer] = useState(59);

  useEffect(() => {
    const interval = setInterval(() => setTimer((state: number) => (state === 0 ? 59 : state - 1)), 1000);

    return () => {
      clearInterval(interval);
    };
  }, []);

  const renderSeconds = () => (timer.toString().length === 2 ? timer.toString() : '0' + timer.toString());

  return (
    <>
      {[Status.Loading, Status.Waiting].includes(state.status) && (
        <div className="fixed inset-0 z-10 bg-black opacity-60" />
      )}
      {[Status.Loading].includes(state.status) && (
        <div className="fixed top-[10rem] left-0 z-20 min-w-[100%]">
          <h2 className="text-16">Checking queue...</h2>
        </div>
      )}
      {[Status.Waiting].includes(state.status) && (
        <div className="fixed top-[10rem] left-0 z-20 min-w-[100%]">
          <h2 className="text-16">
            We are quite busy. <br />
            Approx. time for you to play is:
          </h2>
          <h2 className="my-[1.5rem] text-[3.2rem] font-bold leading-[3.9rem] tracking-[0.1rem]">
            0:{renderSeconds()}
          </h2>
        </div>
      )}
    </>
  );
}

export default Loader;
