import { Status } from 'enums/status';

function Loader({ state }: { state: State }) {
  return (
    <>
      {[Status.Loading, Status.Waiting].includes(state.status) && (
        <div className="fixed inset-0 z-10 bg-black opacity-60" />
      )}
      {[Status.Loading].includes(state.status) && (
        <h2 className="fixed top-[10rem] left-0 z-20 min-w-[100%] text-16">Checking queue...</h2>
      )}
      {[Status.Waiting].includes(state.status) && (
        <h2 className="fixed top-[10rem] left-0 z-20 min-w-[100%] text-16">
          We are quite busy. <br />
          Approx. time for you to play is:
        </h2>
      )}
    </>
  );
}

export default Loader;
