import Image from 'next/image';
import Link from 'next/link';
import { renderIcon } from 'assets/utils';

const renderLink = (name: string, href: string) => (
  <a className="flex justify-center" href={href} target="_blank" rel="noreferrer">
    <div className="flex h-6 items-center">
      <Image className="mr-4" src={renderIcon(name)} alt={`${name} logo`} width={18} height={18} />
      <span className="underline">{name}</span>
    </div>
  </a>
);

function Footer() {
  return (
    <footer className="absolute inset-x-0 bottom-0 flex min-h-[4rem] flex-col items-center justify-between p-6 uppercase text-black lg:flex-row">
      <div className="mb-[0.6rem] flex items-end">
        <span className="mr-1 text-[12px]">©</span>2024 Golem Network. All rights reserved.
      </div>
      <div className="flex flex-col items-center justify-between md:flex-row md:gap-12">
        <div className="mb-[0.6rem] flex items-end">
          <span className="mr-4">Want to give us a feedback?</span>
          {renderLink('discord', 'https://discord.com/channels/684703559954333727')}
        </div>
        <div className="mb-[0.6rem] flex items-end">
          <span className="mr-4">Want to check our code?</span>
          {renderLink('github', 'https://github.com/golemfactory/gpu-on-golem-poc')}
        </div>
        <div className="mb-[0.6rem] flex items-end">
          <Link className="underline" href="/terms">
            Terms of Use
          </Link>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
