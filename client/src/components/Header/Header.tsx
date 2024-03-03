import Image from 'next/image';
import Link from 'next/link';
import { useWeb3Modal, useWeb3ModalAccount } from '@web3modal/ethers/react';
import { renderIcon } from 'assets/utils';
import ellipsis from 'utils/ellipsis';

function Header() {
  const { open } = useWeb3Modal();
  const { address } = useWeb3ModalAccount();

  return (
    <header className="absolute inset-x-0 top-8 flex flex-col items-center justify-between md:flex-row md:px-12 lg:top-12 lg:px-20">
      <Link href="/">
        <Image src={renderIcon('logo')} alt="logo" width={135} height={40} />
      </Link>
      <button className="min-w-[210px] py-[12px] px-[24px] font-normal tracking-[2px]" onClick={() => open()}>
        {address ? ellipsis(address) : 'Connect Wallet'}
      </button>
    </header>
  );
}

export default Header;
