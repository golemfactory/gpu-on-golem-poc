import { ReactNode, useEffect, useState } from 'react';

const facts = [
  'The Golem Network is a revolutionary open-source platform that harnesses the power of decentralization for accessing and sharing computer resources.',
  'Golem runs various incentive programs. Join the community and build Golem with other users from all over the world.',
  'Our mission is to create 𝙖𝙣 𝙤𝙥𝙚𝙣-𝙨𝙤𝙪𝙧𝙘𝙚 𝙥𝙡𝙖𝙩𝙛𝙤𝙧𝙢 that meets the challenges of the upcoming technology era. We believe that 𝙤𝙪𝙧 𝙧𝙚𝙨𝙚𝙖𝙧𝙘𝙝 𝙖𝙣𝙙 𝙙𝙚𝙫𝙚𝙡𝙤𝙥𝙢𝙚𝙣𝙩 activities will evolutionarily influence the shape of emerging new projects and allow many more to be built on top of our efforts.',
  "Golem's new implementation is called Yagna.",
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
