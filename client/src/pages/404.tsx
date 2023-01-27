import { useRouter } from 'next/router';
import { Background, Error, Layout } from 'components';

function ErrorPage() {
  const router = useRouter();

  const handleClick = () => router.push('/');

  return (
    <Layout>
      <Background />
      <Error heading="404" text="This page doesn't exist." button={{ label: 'Go Home', onClick: handleClick }} />
    </Layout>
  );
}

export default ErrorPage;
