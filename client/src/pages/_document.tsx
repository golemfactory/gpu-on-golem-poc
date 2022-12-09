import { Html, Head, Main, NextScript } from 'next/document';

function Document() {
  return (
    <Html>
      <Head>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto+Mono:500&" />
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Inter:500,700" />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}

export default Document;
