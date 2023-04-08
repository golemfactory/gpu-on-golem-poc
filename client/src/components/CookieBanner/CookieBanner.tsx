'use client';

import { useEffect } from 'react';
import { useLocalStorage, useToggle } from 'react-use';
import Link from 'next/link';
import { gaEvent } from 'components';

function CookieBanner() {
  const [value, update] = useLocalStorage<boolean>('golem-cookie-consent', undefined);
  const [on, toggle] = useToggle(false);

  useEffect(() => {
    toggle(typeof value === 'undefined');

    gaEvent('cookie_consent', {
      analytics_storage: value ? 'granted' : 'denied',
    });
  }, [value]);

  return on ? (
    <div className="fixed inset-x-0 bottom-[5rem] z-10 flex flex-col bg-black p-[2rem]">
      <p className="mb-[1.6rem] text-left text-18"> Let us know you agree to cookies!</p>
      <p className="mb-[2.4rem] text-left text-14">
        We use{' '}
        <Link href="/terms" className="text-blue">
          cookies
        </Link>{' '}
        to give you the best online experience. Please let us know if you agree to all of these cookies.
      </p>
      <div className="mb-[1.6rem] flex justify-end">
        <button className="mr-[1rem] bg-white p-[1rem] text-14 text-black" onClick={() => update(false)}>
          Deny
        </button>
        <button className="p-[1rem] text-14" onClick={() => update(true)}>
          Allow
        </button>
      </div>
    </div>
  ) : null;
}

export default CookieBanner;
