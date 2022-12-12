import Image from 'next/image';

function Header() {
  return (
    <header className="fixed inset-x-0 top-[2rem] px-[5rem] lg:top-[6rem]">
      <Image className="mx-auto lg:mx-0" src="/logo.svg" alt="logo" width={88} height={64} />
    </header>
  );
}

export default Header;
