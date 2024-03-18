'use client';

import { useEffect, useState } from 'react';
import { useWeb3ModalAccount, useWeb3ModalProvider } from '@web3modal/ethers/react';
import { BrowserProvider, Contract, formatUnits } from 'ethers';
import abi from './erc20.json';

enum SupportedChains {
  Ethereum = 1,
  Polygon = 137,
}

const glm_address = {
  [SupportedChains.Ethereum]: '0x7DD9c5Cba05E151C895FDe1CF355C9A1D5DA6429',
  [SupportedChains.Polygon]: '0x0B220b82F3eA3B7F6d9A1D8ab58930C064A2b5Bf',
};

export const useBalance = () => {
  const { address, chainId } = useWeb3ModalAccount();
  const { walletProvider } = useWeb3ModalProvider();

  const [balance, setBalance] = useState<string | null>(null);

  const handleBalance = async () => {
    // @ts-ignore
    const contract_address = glm_address[chainId];

    const provider = new BrowserProvider(walletProvider!);
    const contract = new Contract(contract_address, abi, provider);

    try {
      const balance = await contract.balanceOf(address);

      setBalance(parseFloat(formatUnits(balance)).toFixed(2));
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    walletProvider &&
      address &&
      [SupportedChains.Ethereum, SupportedChains.Polygon].includes(chainId!) &&
      handleBalance();
  }, [walletProvider, address, chainId]);

  return { balance };
};
