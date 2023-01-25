import Image from 'next/image';
import { renderIcon } from 'assets/utils';

const renderLink = (name: string, href: string) => (
  <a className="mx-[2rem] flex justify-center" href={href} target="_blank" rel="noreferrer">
    <div className="flex items-center hover:text-white">
      <Image className="mr-[1rem]" src={renderIcon(name)} alt={`${name} logo`} width={18} height={18} />
      <span className="uppercase underline">{name}</span>
    </div>
  </a>
);

function Footer() {
  return (
    <footer className="container absolute inset-x-0 bottom-0 flex min-h-[9rem] max-w-prose flex-col p-[1.5rem]">
      <span className="mb-[1.6rem] text-[1.2rem]">Want to check our code?</span>
      <div className="text-[1rem]">{renderLink('github', 'https://github.com/golemfactory/gpu-on-golem-poc')}</div>
    </footer>
  );
}

export default Footer;
