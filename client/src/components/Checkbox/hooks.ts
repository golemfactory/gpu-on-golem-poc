import { useToggle } from 'react-use';
import { useFormError } from 'components';

export function useCheckbox(): useCheckboxType & { onError: onErrorType } {
  const [on, toggle] = useToggle(false);
  const { error, onError } = useFormError();

  const handleChange = () => {
    toggle();
    onError();
  };

  return {
    on,
    onChange: handleChange,
    onError,
    error,
  };
}
