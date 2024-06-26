import { Provider } from 'react-redux';
import type { AppProps } from 'next/app';
import Head from 'next/head';
import Script from 'next/script';
import wrapper from 'store';
import 'styles/globals.css';
import GoogleAnalytics from 'services/GoogleAnalytics';
import Web3ModalProvider from 'services/Web3Modal';

function App({ Component, pageProps, ...rest }: AppProps) {
  const { store } = wrapper.useWrappedStore(rest);

  return (
    <>
      <Head>
        <title>{process.env.NEXT_PUBLIC_PROJECT_TITLE}</title>
        <meta name="title" content={process.env.NEXT_PUBLIC_PROJECT_TITLE} />
        <meta name="description" content={process.env.NEXT_PUBLIC_PROJECT_DESCRIPTION} />
        <meta property="og:title" content={process.env.NEXT_PUBLIC_PROJECT_TITLE} />
        <meta property="og:description" content={process.env.NEXT_PUBLIC_PROJECT_DESCRIPTION} />
        <meta property="og:type" content="website" />
        <meta property="og:image" content="https://image.golem.network/static/image.png" />
        <meta property="og:image:width" content="1200" />
        <meta property="og:image:height" content="630" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
      </Head>
      <Script
        id="cookieyes"
        type="text/javascript"
        src="https://cdn-cookieyes.com/client_data/8d9e86c3dd88742506b050d9/script.js"
      />
      <GoogleAnalytics />
      <Provider store={store}>
        <Web3ModalProvider>
          <Component {...pageProps} />
        </Web3ModalProvider>
      </Provider>
    </>
  );
}

export default App;
