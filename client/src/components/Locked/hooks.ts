import { useEffect, useState } from 'react';
import { useLocalStorage } from 'react-use';
import { useBalance } from 'hooks/useBalance';

export const useLocked = () => {
  const { balance } = useBalance();
  const [until, update] = useLocalStorage<number | null>('golem-locked-until', undefined);
  const locked = balance === null || parseFloat(balance!) < parseFloat(process.env.NEXT_PUBLIC_GLM_LIMIT!);
  const unlocked = balance !== null && parseFloat(balance!) >= parseFloat(process.env.NEXT_PUBLIC_GLM_LIMIT!);

  const [, setCurrentTime] = useState(Date.now());

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(Date.now());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    if (unlocked || (until !== null && until! < Date.now())) {
      update(null);
    }
  }, [unlocked, until]);

  return {
    locked,
    unlocked,
    until,
    onUpdate: (value: number | null) => update(value),
  };
};
