import { useEffect, useRef } from 'react';
import { useSelector } from 'react-redux';
import { selectData } from 'slices/data';

export function useCountdown() {
  const data = useSelector(selectData);

  const countdown = useRef<number>();

  useEffect(() => {
    if (data?.progress === 0 && data?.eta) {
      countdown.current = Date.now() + data.eta * 1000;
    }
  }, [data?.eta, data?.progress]);

  return countdown;
}
