import { useLocalStorage } from 'react-use';

export function useTermsRemember() {
  const [value, update] = useLocalStorage<boolean>('golem-terms-remember', false);

  const handleChange = (value: boolean) => update(value);

  return { value: value ?? false, onChange: handleChange };
}
