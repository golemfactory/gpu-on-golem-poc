import { ReactNode } from 'react';
import { Footer, Header } from 'components';

function Layout({ children }: { children: ReactNode }) {
  return (
    <>
      <Header />
      <main className="container flex min-h-screen max-w-[74rem] flex-col pb-[9rem]">{children}</main>
      <Footer />
    </>
  );
}

export default Layout;
