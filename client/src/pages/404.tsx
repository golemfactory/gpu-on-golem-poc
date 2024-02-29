import { useRouter } from 'next/router';
import { Error, Layout } from 'components';

function ErrorPage() {
  const router = useRouter();

  const handleClick = () => router.push('/');

  return (
    <Layout>
      <Error heading="404" text="This page doesn't exist." button={{ label: 'Go to homepage', onClick: handleClick }} />
    </Layout>
  );
}

export default ErrorPage;
