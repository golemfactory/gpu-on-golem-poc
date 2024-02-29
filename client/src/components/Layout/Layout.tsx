import { PropsWithChildren } from 'react';
import backgroundJPEG from 'assets/background.jpeg';
import { Footer, Header } from 'components';

function Layout({ children, footer = true }: { footer?: boolean } & PropsWithChildren) {
  return (
    <>
      <Header />
      <main
        className="bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: footer ? `url(${backgroundJPEG.src})` : '' }}
      >
        <div className="mx-auto flex min-h-screen w-[90%] max-w-[70rem] flex-col pb-[11rem] md:w-full">{children}</div>
      </main>
      {footer && <Footer />}
    </>
  );
}

export default Layout;
