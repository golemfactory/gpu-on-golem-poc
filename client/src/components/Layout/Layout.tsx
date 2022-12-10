import { ReactNode } from 'react';
import { Footer } from 'components';

function Layout({ children }: { children: ReactNode }) {
  return (
    <>
      <main className="container flex min-h-screen max-w-screen-md flex-col pb-[9rem]">{children}</main>
      <Footer />
    </>
  );
}

export default Layout;
