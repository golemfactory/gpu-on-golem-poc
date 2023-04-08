import type { AppProps } from 'next/app';
import Head from 'next/head';
import { Provider } from 'react-redux';
import wrapper from 'store';
import 'styles/globals.css';
import { GoogleAnalytics } from 'components';

function App({ Component, pageProps, ...rest }: AppProps) {
  const { store } = wrapper.useWrappedStore(rest);

  return (
    <>
      <Head>
        <title>GPU on Golem</title>
      </Head>
      <GoogleAnalytics />
      <Provider store={store}>
        <Component {...pageProps} />
      </Provider>
    </>
  );
}

export default App;
