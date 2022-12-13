import { FormEvent, useEffect, useState } from 'react';
import { adjectives, animals, colors, uniqueNamesGenerator } from 'unique-names-generator';
import { Api } from 'enums/api';
import { Status } from 'enums/status';
import queryBuild from 'utils/query';
import url from 'utils/url';
import { nouns, verbs } from './dictionaries';

const example = () =>
  uniqueNamesGenerator({
    dictionaries: [adjectives, animals, verbs, colors, nouns],
    separator: ' ',
    length: 5,
  });

export function useForm(dispatch: (action: Action) => void): useFormType {
  const [value, setValue] = useState<string>('');
  const [error, setError] = useState<string | undefined>(undefined);

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

  const handleChange = async (e: FormEvent) => {
    const value = (e.target as HTMLInputElement).value;

    setValue(value);
    setError(undefined);
  };

  const handleSubmit = async (e: any) => {
    e.preventDefault();

    if (!value.length) return setError('This field is required');

    const response = await fetch(url(Api.txt2img, false), {
      body: queryBuild({ prompt: value }),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      method: 'POST',
    });

    if (response.status === 404) return dispatch({ type: Status.Error });

    const result = await response.json();

    if (result.detail) return setError(result.detail[0].msg);
    else return dispatch({ type: Status.Processing, payload: result.job_id });
  };

  return {
    value,
    onChange: handleChange,
    error,
    onSubmit: handleSubmit,
    onExample: handleExample,
  };
}
