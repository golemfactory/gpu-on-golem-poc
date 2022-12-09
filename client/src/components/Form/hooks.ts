import { FormEvent, useState } from 'react';
import { Status } from 'enums/status';
import queryBuild from 'utils/query';

export function useForm(dispatch: (action: Action) => void): useFormType {
  const example = 'grey hair man in the mountains wearing red jacket sci-fi';
  const [value, setValue] = useState<string>(example);
  const [error, setError] = useState<string | undefined>(undefined);

  const handleChange = async (e: FormEvent) => {
    const value = (e.target as HTMLInputElement).value;

    setValue(value);
    setError(undefined);
  };

  const handleSubmit = async (e: any) => {
    e.preventDefault();

    if (!value.length) return setError('This field is required');

    const response = await fetch(`${process.env.NEXT_PUBLIC_API}txt2img/`, {
      body: queryBuild({ prompt: value }),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      method: 'POST',
    });
    const result = await response.json();

    if (result.detail) return setError(result.detail[0].msg);
    else return dispatch({ type: Status.Processing, payload: result.job_id });
  };

  const handleReset = () => {
    dispatch({ type: Status.Ready });
    setValue(example);
  };

  return {
    example,
    value,
    onChange: handleChange,
    error,
    onSubmit: handleSubmit,
    onReset: handleReset,
  };
}
