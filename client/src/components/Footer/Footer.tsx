import Image from 'next/image';
import Link from 'next/link';
import { renderIcon } from 'assets/utils';

const renderLink = (name: string, href: string) => (
  <a className="flex justify-center" href={href} target="_blank" rel="noreferrer">
    <div className="flex h-[1.5rem] items-center hover:text-white">
      <Image className="mr-[1rem]" src={renderIcon(name)} alt={`${name} logo`} width={18} height={18} />
      <span className="uppercase underline">{name}</span>
    </div>
  </a>
);

function Footer() {
  return (
    <footer className="container absolute inset-x-0 bottom-0 flex min-h-[4rem] flex-col justify-between p-[1.5rem] sm:flex-row md:max-w-prose">
      <div className="mb-[0.6rem] flex items-end">
        <span className="mr-[1rem] text-[1.2rem]">Want to check our code?</span>
        {renderLink('github', 'https://github.com/golemfactory/gpu-on-golem-poc')}
      </div>
      <div className="mb-[0.6rem] flex items-end">
        <span className="mr-[1rem] text-[1.2rem]">Read:</span>
        <Link className="uppercase underline" href="/terms">
          Terms of Use
        </Link>
      </div>
    </footer>
  );
}

export default Footer;
