import { ReactNode } from 'react';

function Hero({ children }: { children: ReactNode }) {
  return (
    <div className="mt-[20rem]">
      <h1 className="mb-[5.7rem] text-24 md:text-34">
        Use AI harnessed by the decentralized Golem Network platform to produce artwork from keywords.
      </h1>
      {children}
    </div>
  );
}

export default Hero;
