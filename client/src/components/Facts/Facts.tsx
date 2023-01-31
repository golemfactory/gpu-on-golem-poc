import { ReactNode, useEffect, useState } from 'react';

const facts = [
  'Golem is a decentralized, open-source platform that allows users to rent out their computing power to others.',
  "Golem's native cryptocurrency, GLM, is used as a form of payment for renting computing power on the network.",
  'Golem runs various incentive programs. Join the community and build Golem together with other users from all over the world.',
  "The Golem's main product is Yagna.",
  'You can find the entire Golem code on our GitHub.',
];

function Facts() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => setIndex((state: number) => (state !== facts.length - 1 ? state + 1 : 0)), 5000);

    return () => {
      clearInterval(interval);
    };
  }, []);

  const renderText = (children: ReactNode) => (
    <p className="mt-[5.7rem] mb-[2.4rem] min-h-[9.5rem] text-14">{children}</p>
  );

  return renderText(
    <span className="mt-[8rem] md:mt-0">
      Facts:
      <br />
      <br />
      {facts[index]}
    </span>,
  );
}

export default Facts;
