import Image from 'next/image';

function Result({ data, value, onReset }: { data?: Data; value: string; onReset?: () => void }) {
  return (
    <div className="my-[5rem]">
      <h2 className="text-36">Result for:</h2>
      <h3 className="mt-[1.2rem] mb-[2.4rem] text-12 text-[#9c9c9c]">{value}</h3>
      <Image
        className="mx-auto"
        src={`${process.env.NEXT_PUBLIC_API}${data?.img_url}`}
        alt={value}
        width={512}
        height={512}
      />
      <p className="mt-[5.7rem] mb-[2.4rem] text-14">
        We hope you enjoy your results! Drop us a line on our Discord chat and share your experience :)
      </p>
      <div>
        <button className="button bg-white text-black" onClick={onReset}>
          Start over
        </button>
        <button className="button">Chat with us!</button>
      </div>
    </div>
  );
}

export default Result;
