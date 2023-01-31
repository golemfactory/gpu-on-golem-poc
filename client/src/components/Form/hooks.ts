import { FormEvent, useEffect, useRef, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { adjectives, animals, colors, uniqueNamesGenerator } from 'unique-names-generator';
import { Api } from 'enums/api';
import gaEvent from 'lib/ga';
import { selectJobId, setJobId } from 'slices/data';
import { setQueue } from 'slices/queue';
import { setStatus } from 'slices/status';
import { useFetch } from 'utils/hooks';
import queryBuild from 'utils/query';
import url from 'utils/url';
import { nouns, verbs } from './dictionaries';

const example = () =>
  uniqueNamesGenerator({
    dictionaries: [adjectives, animals, verbs, colors, nouns],
    separator: ' ',
    length: 5,
  });

export function useForm(): useFormType {
  const appDispatch = useDispatch();
  const job_id = useSelector(selectJobId);

  const [value, setValue] = useState<string>('');
  const [error, setError] = useState<string | undefined>(undefined);

  const disabled = !!job_id;

  const generated = useRef(value);

  const handleGenerate = () => {
    const prompt = example();

    setValue(prompt);
    generated.current = prompt;
  };

  useEffect(() => {
    handleGenerate();

    return () => {
      setValue('');
    };
  }, []);

  const handleExample = () => {
    handleGenerate();
    setError(undefined);
  };

  const handleClear = () => {
    setValue('');
    setError(undefined);
  };

  const handleChange = async (e: FormEvent) => {
    const value = (e.target as HTMLInputElement).value;

    setValue(value);
    setError(undefined);
  };

  const handlePost = useFetch();

  const handleSubmit = async (e: HTMLFormElement) => {
    e.preventDefault();

    if (!value.length) return setError('This field is required');

    const result = await handlePost(url(Api.txt2img, false), {
      body: queryBuild({ prompt: value }),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      method: 'POST',
    });

    gaEvent('txt2img_submit', {
      generator_phrase: generated.current === value,
    });

    if (!result) return;
    else if (result.detail) return setError(result.detail[0].msg);
    else {
      appDispatch(setStatus(result.status));
      appDispatch(setQueue(result.queue_position));
      appDispatch(setJobId(result.job_id));
    }
  };

  return {
    value,
    onChange: handleChange,
    error,
    disabled,
    onSubmit: handleSubmit,
    onExample: handleExample,
    onClear: handleClear,
  };
}
