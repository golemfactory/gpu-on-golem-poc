import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { Api } from 'enums/api';
import { Status } from 'enums/status';
import { Error, Layout, Result } from 'components';
import { resetData, setData } from 'slices/data';
import { selectError, setError } from 'slices/error';
import { setStatus } from 'slices/status';
import { useStatusState } from 'utils/hooks';
import url from 'utils/url';

export async function getServerSideProps({ params }: { params: { id: string } }) {
  const data = await fetch(url(`${Api.txt2img}${params.id}/`, false)).then((response) => response.json());

  return { props: { data } };
}

function Page(props: { data: Data }) {
  const router = useRouter();
  const dispatch = useDispatch();

  useEffect(() => {
    if (props.data.image) {
      dispatch(
        setData({
          image: props.data.image,
          job_id: props.data.job_id,
        }),
      );
      dispatch(setStatus(Status.Finished));
    } else {
      dispatch(setStatus(Status.Error));
      dispatch(setError(404));
    }
  }, [props.data]);

  const error = useSelector(selectError);

  const { forState } = useStatusState();

  const handleReset = () => {
    dispatch(setStatus(Status.Ready));
    dispatch(resetData());
  };

  const handleError = () => {
    router.push('/');
    handleReset();
  };

  return (
    <>
      <Head>
        <meta name="twitter:card" content="summary_large_image" />
        <meta property="og:image" content={`https://${process.env.NEXT_PUBLIC_HOSTNAME}/${props.data.image}`} />
        <meta property="og:image:width" content="1024" />
        <meta property="og:image:height" content="1024" />
      </Head>
      <Layout onReset={handleReset}>
        {forState([Status.Finished]) && <Result value="" onReset={handleReset} />}
        {forState([Status.Error]) && (
          <Error
            {...(error === 404 && { heading: 'Not found.', text: 'This image is not available.' })}
            button={{ label: 'Try again', onClick: handleError }}
          />
        )}
      </Layout>
    </>
  );
}

export default Page;
