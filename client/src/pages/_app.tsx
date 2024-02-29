import { Provider } from 'react-redux';
import type { AppProps } from 'next/app';
import Head from 'next/head';
import wrapper from 'store';
import 'styles/globals.css';
import { CookieBanner } from 'components';
import GoogleAnalytics from 'services/GoogleAnalytics';

function App({ Component, pageProps, ...rest }: AppProps) {
  const { store } = wrapper.useWrappedStore(rest);

  return (
    <>
      <Head>
        <title>{process.env.NEXT_PUBLIC_PROJECT_NAME}</title>
      </Head>
      <GoogleAnalytics />
      <CookieBanner />
      <Provider store={store}>
        <Component {...pageProps} />
      </Provider>
    </>
  );
}

export default App;
