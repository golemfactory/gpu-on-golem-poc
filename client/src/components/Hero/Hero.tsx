import { PropsWithChildren } from 'react';

function Hero({ children }: PropsWithChildren) {
  return (
    <div className="mt-80 flex flex-col gap-10">
      <h1 className="text-24 md:text-34">Use AI harnessed by the Golem Network to produce artwork from keywords</h1>
      <p className="text-14 font-light">
        Link your wallet with a minimum of{' '}
        <span className="text-blue underline">{process.env.NEXT_PUBLIC_GLM_LIMIT} GLM</span> to unlock unlimited access
        to Golem's AI Image Generator.
      </p>
      {children}
    </div>
  );
}

export default Hero;
