'use client';

import { createWeb3Modal, defaultConfig } from '@web3modal/ethers/react';
import chains from './chains';

const projectId = process.env.NEXT_PUBLIC_PROJECT_ID;

if (!projectId) throw new Error('Project ID is not defined');

const metadata = {
  name: process.env.NEXT_PUBLIC_PROJECT_NAME ?? '',
  description: '',
  url: 'https://image.golem.network/',
  icons: [],
};

createWeb3Modal({
  ethersConfig: defaultConfig({ metadata }),
  chains,
  projectId,
  themeMode: 'light',
});

function Web3ModalProvider({ children }: { children: JSX.Element }) {
  return children;
}

export default Web3ModalProvider;
