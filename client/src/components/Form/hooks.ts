import { FormEvent, useRef, useState } from 'react';
import { useEffectOnce } from 'react-use';
import { useDispatch, useSelector } from 'react-redux';
import { adjectives, animals, colors, uniqueNamesGenerator } from 'unique-names-generator';
import { Api } from 'enums/api';
import gaEvent from 'lib/ga';
import { useCheckbox } from 'components';
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

export function useFormError(): useErrorType {
  const [error, setError] = useState<string | undefined>(undefined);

  const handleError = (error?: string) => setError(error ?? undefined);

  return {
    error,
    onError: handleError,
  };
}

export function useForm(): useFormType {
  const dispatch = useDispatch();
  const job_id = useSelector(selectJobId);

  const [value, setValue] = useState<string>('');
  const { error, onError } = useFormError();
  const terms = useCheckbox();

  const disabled = !!job_id;

  const generated = useRef(value);

  const handleGenerate = () => {
    const prompt = example();

    setValue(prompt);
    generated.current = prompt;
  };

  useEffectOnce(() => {
    handleGenerate();

    return () => {
      setValue('');
    };
  });

  const handleExample = () => {
    handleGenerate();
    onError();
  };

  const handleClear = () => {
    setValue('');
    onError();
  };

  const handleChange = async (e: FormEvent) => {
    const value = (e.target as HTMLInputElement).value;

    setValue(value);
    onError();
  };

  const handlePost = useFetch();

  const handleSubmit = async (e: HTMLFormElement) => {
    e.preventDefault();

    if (!value.length) return onError('This field is required');
    if (!terms.on) return terms.onError('Consent is required');

    const result = await handlePost(url(Api.txt2img, false), {
      body: queryBuild({ prompt: value }),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      method: 'POST',
    });

    gaEvent('txt2img_submit', {
      generator_phrase: generated.current === value,
    });

    if (!result) return;
    else if (result.detail) return onError(result.detail[0].msg);
    else {
      dispatch(setStatus(result.status));
      dispatch(setQueue(result.queue_position));
      dispatch(setJobId(result.job_id));
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
    terms,
  };
}
