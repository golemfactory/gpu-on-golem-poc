import { useEffect, useRef } from 'react';

export function useCountdown(data?: Data) {
  const countdown = useRef<number>();

  useEffect(() => {
    if (data?.progress === 0) {
      countdown.current = Date.now() + data?.eta * 1000;
    }
  }, [data?.eta, data?.progress]);

  return countdown;
}
