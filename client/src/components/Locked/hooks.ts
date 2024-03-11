import { useEffect, useState } from 'react';
import { useLocalStorage } from 'react-use';
import { useWeb3ModalProvider } from '@web3modal/ethers/react';
import { useBalance } from 'hooks/useBalance';

export const useLocked = () => {
  const { walletProvider } = useWeb3ModalProvider();
  const { balance } = useBalance();
  const [count, updateCount] = useLocalStorage<number>('golem-locked-count', 0);
  const [until, updateUntil] = useLocalStorage<number | null>('golem-locked-until', null);
  const [locked, setLocked] = useState(true);

  useEffect(() => {
    if (!walletProvider) {
      setLocked(true);
    } else {
      setLocked(!(parseFloat(balance!) >= parseFloat(process.env.NEXT_PUBLIC_GLM_LIMIT!)));
    }
  }, [walletProvider, balance]);

  const [, setCurrentTime] = useState(Date.now());

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(Date.now());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    if (!locked || (until !== null && until! < Date.now())) {
      updateCount(0);
      updateUntil(null);
    }
  }, [locked, until]);

  return {
    limited: count! >= Number(process.env.NEXT_PUBLIC_LOCK_COUNT) && !!until,
    locked,
    count,
    until,
    onUpdate: (until: number | null, count: number) => {
      updateCount(count);
      updateUntil(until);
    },
  };
};
