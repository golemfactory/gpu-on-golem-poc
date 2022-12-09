import { ReactNode } from 'react';

function Layout({ children }: { children: ReactNode }) {
  return <main className="container flex min-h-screen max-w-screen-md flex-col">{children}</main>;
}

export default Layout;
