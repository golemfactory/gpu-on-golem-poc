import { useRouter } from 'next/router';
import { Error, Layout } from 'components';

function ErrorPage() {
  const router = useRouter();

  const handleClick = () => router.push('/');

  return (
    <Layout>
      <div className="mt-[20rem]">
        <h1 className="text-[9.6rem] font-bold leading-[11.6rem] -tracking-[0.15rem]">404</h1>
        <Error label="Go Home" onClick={handleClick} />
      </div>
    </Layout>
  );
}

export default ErrorPage;
