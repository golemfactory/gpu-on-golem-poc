import Image from 'next/image';

const renderLink = (name: string, href: string) => (
  <a className="mx-[2rem] flex justify-center" href={href} target="_blank" rel="noreferrer">
    <div className="flex items-center">
      <Image className="mr-[1rem]" src={`/${name}.svg`} alt={`${name} logo`} width={18} height={18} />
      <span className="uppercase underline">{name}</span>
    </div>
  </a>
);

function Footer() {
  return (
    <footer className="container absolute inset-x-0 bottom-0 flex min-h-[9rem] max-w-prose flex-col p-[1.5rem]">
      <span className="mb-[1.6rem] text-[1.2rem]">Stay in touch:</span>
      <div className="columns-3 text-[1rem]">
        {renderLink('discord', 'https://chat.golem.network/')}
        {renderLink('github', 'https://github.com/golemfactory/')}
        {renderLink('twitter', 'https://twitter.com/golemproject/')}
      </div>
    </footer>
  );
}

export default Footer;
