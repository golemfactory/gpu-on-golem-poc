import { ReactNode } from 'react';
import { Footer, Header } from 'components';

function Layout({ children, footer = true }: { children: ReactNode; footer?: boolean }) {
  return (
    <>
      <Header />
      <main className="container flex min-h-screen max-w-[74rem] flex-col pb-[9rem]">{children}</main>
      {footer && <Footer />}
    </>
  );
}

export default Layout;
