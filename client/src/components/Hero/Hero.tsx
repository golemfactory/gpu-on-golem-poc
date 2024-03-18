import { PropsWithChildren } from 'react';

function Hero({ children }: PropsWithChildren) {
  return (
    <div className="mt-60 flex flex-col gap-10 md:mt-80">
      <h1 className="text-24 md:text-34">{process.env.NEXT_PUBLIC_PROJECT_TITLE}</h1>
      <p className="text-14 font-light">
        Connect your wallet containing at least{' '}
        <span className="text-blue underline">{process.env.NEXT_PUBLIC_GLM_LIMIT} GLM</span> to unlock FREE and
        unlimited access to Golem's AI Image Generator.
      </p>
      {children}
    </div>
  );
}

export default Hero;
