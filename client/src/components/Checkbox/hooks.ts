import { useToggle } from 'react-use';
import { useFormError } from 'components';

export function useCheckbox(initialValue: boolean): useCheckboxType & { onError: onErrorType } {
  const [on, toggle] = useToggle(initialValue);
  const { error, onError } = useFormError();

  const handleChange = () => {
    toggle();
    onError();
  };

  return {
    on,
    toggle,
    onChange: handleChange,
    onError,
    error,
  };
}
