import { FormEvent, useEffect, useState } from 'react';
import { adjectives, animals, colors, uniqueNamesGenerator } from 'unique-names-generator';
import { Api } from 'enums/api';
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

export function useForm(state: State, dispatch: (action: Action) => void): useFormType {
  const [value, setValue] = useState<string>('');
  const [error, setError] = useState<string | undefined>(undefined);

  const disabled = !!state.job_id;

  useEffect(() => {
    setValue(example());

    return () => {
      setValue('');
    };
  }, []);

  const handleExample = () => {
    setValue(example());
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

  const handlePost = useFetch(dispatch);

  const handleSubmit = async (e: HTMLFormElement) => {
    e.preventDefault();

    if (!value.length) return setError('This field is required');

    const result = await handlePost(url(Api.txt2img, false), {
      body: queryBuild({ prompt: value }),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      method: 'POST',
    });

    if (result.detail) return setError(result.detail[0].msg);
    else return dispatch({ type: result.status, payload: result.job_id });
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
