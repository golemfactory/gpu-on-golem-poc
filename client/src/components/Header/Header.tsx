import Image from 'next/image';
import Link from 'next/link';
import { renderIcon } from 'assets/utils';

function Header() {
  return (
    <header className="absolute inset-x-0 top-8 flex flex-col items-center justify-between md:flex-row md:px-12 lg:top-12 lg:px-20">
      <Link href="/">
        <Image src={renderIcon('logo')} alt="logo" width={135} height={40} />
      </Link>
    </header>
  );
}

export default Header;
