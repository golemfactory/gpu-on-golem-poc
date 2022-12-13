function Error({ label, onClick }: { label: string; onClick: () => void }) {
  return (
    <>
      <p className="mt-[5.7rem] mb-[2.4rem] text-14">Hey! It seems that something went totally wrong :(</p>
      <button className="button bg-white text-black" onClick={onClick}>
        {label}
      </button>
    </>
  );
}

export default Error;
