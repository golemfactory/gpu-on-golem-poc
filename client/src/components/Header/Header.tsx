'use client';

import Image from 'next/image';
import Link from 'next/link';
import { useWeb3Modal, useWeb3ModalAccount } from '@web3modal/ethers/react';
import { useBalance } from 'hooks/useBalance';
import { renderIcon } from 'assets/utils';
import ellipsis from 'utils/ellipsis';

function Header() {
  const { open } = useWeb3Modal();
  const { address } = useWeb3ModalAccount();

  const { balance } = useBalance();

  const renderBalance = () => `${address && balance ? balance : '0.00'} GLM`;

  return (
    <>
      <header className="absolute inset-x-0 top-8 flex items-center justify-between px-12 md:flex-row lg:top-12 lg:px-20">
        <Link href="/">
          <Image
            className="max-w-[90px] md:max-w-[135px]"
            src={renderIcon('logo')}
            alt="logo"
            width={135}
            height={40}
          />
        </Link>
        <div className="flex gap-[3.2rem]">
          <div className="hidden items-center text-[14px] md:flex">
            <Image className="mr-4" src={renderIcon('glm')} alt="glm" width={18} height={18} />
            {renderBalance()}
          </div>
          <div className="flex gap-[0.8rem]">
            {/*<button className="hidden items-center bg-transparent py-[12px] px-[24px] font-semibold tracking-[2px] text-blue hover:bg-ghost md:flex">*/}
            {/*  <Image className="mr-4" src={renderIcon('cart')} alt="glm" width={12} height={12} />*/}
            {/*  Buy GLM*/}
            {/*</button>*/}
            <button className="min-w-[185px] py-[12px] px-[24px] font-semibold tracking-[2px]" onClick={() => open()}>
              {address ? ellipsis(address) : 'Connect Wallet'}
            </button>
          </div>
        </div>
      </header>
      <div className="fixed inset-x-0 bottom-0 z-10 flex justify-between bg-white p-[12px] md:hidden">
        <div className="flex items-center text-[14px]">
          <Image className="mr-4" src={renderIcon('glm')} alt="glm" width={18} height={18} />
          {renderBalance()}
        </div>
        {/*<button className="flex items-center bg-transparent py-[12px] px-[24px] font-semibold tracking-[2px] text-blue hover:bg-ghost">*/}
        {/*  <Image className="mr-4" src={renderIcon('cart')} alt="glm" width={12} height={12} />*/}
        {/*  Buy GLM*/}
        {/*</button>*/}
      </div>
    </>
  );
}

export default Header;
