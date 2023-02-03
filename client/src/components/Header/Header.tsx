import Image from 'next/image';
import Link from 'next/link';
import { renderIcon } from 'assets/utils';

function Header() {
  return (
    <header className="absolute inset-x-0 top-[2rem] flex flex-col items-center justify-between md:flex-row md:px-[3rem] lg:top-[3rem] lg:px-[5rem]">
      <Link href="/">
        <Image src={renderIcon('logo')} alt="logo" width={250} height={94} />
      </Link>
      <h2 className="mt-[2rem] font-mono text-12 md:mt-0">Golem GPU PoC with Stable Diffusion use case</h2>
    </header>
  );
}

export default Header;
