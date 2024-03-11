import { Provider } from 'react-redux';
import type { AppProps } from 'next/app';
import Head from 'next/head';
import wrapper from 'store';
import 'styles/globals.css';
import { CookieBanner } from 'components';
import GoogleAnalytics from 'services/GoogleAnalytics';
import Web3ModalProvider from 'services/Web3Modal';

function App({ Component, pageProps, ...rest }: AppProps) {
  const { store } = wrapper.useWrappedStore(rest);

  return (
    <>
      <Head>
        <title>{process.env.NEXT_PUBLIC_PROJECT_NAME}</title>
        <meta name="title" content={process.env.NEXT_PUBLIC_PROJECT_NAME} />
        <meta name="description" content="Use AI harnessed by the Golem Network to produce artwork from keywords." />
      </Head>
      <GoogleAnalytics />
      <CookieBanner />
      <Provider store={store}>
        <Web3ModalProvider>
          <Component {...pageProps} />
        </Web3ModalProvider>
      </Provider>
    </>
  );
}

export default App;
