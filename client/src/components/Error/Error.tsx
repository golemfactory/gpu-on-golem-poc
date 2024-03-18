function Error({
  heading,
  text,
  button: { label, onClick },
}: {
  heading?: string;
  text?: string;
  button: { label: string; onClick: Noop };
}) {
  return (
    <div className="mt-[20rem]">
      {heading && (
        <h1 className="text-[5.6rem] font-bold leading-[5.6rem] -tracking-[0.15rem] text-blue md:text-[7.6rem] md:leading-[11.6rem]">
          {heading}
        </h1>
      )}
      <p className="mt-[5.7rem] mb-[2.4rem] text-14">{text ?? 'Hey! It seems that something went totally wrong.'}</p>
      <button className="py-[12px] px-[60px] text-14 tracking-[2px]" onClick={onClick}>
        {label}
      </button>
    </div>
  );
}

export default Error;
