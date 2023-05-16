import { useEffect } from 'react';
import { Checkbox, Tooltip, useCheckbox, useTermsRemember } from 'components';

function Terms({ disabled, terms }: { disabled: boolean; terms: useCheckboxType }) {
  const terms_remember = useTermsRemember();
  const remember = useCheckbox(terms_remember.value);

  useEffect(() => {
    terms_remember.value && !terms.on && remember.toggle();
  }, [terms.on]);

  useEffect(() => {
    terms_remember.onChange(remember.on);
  }, [remember.on]);

  return (
    <div className="flex w-[19rem] items-center justify-between">
      <Checkbox name="terms" label="I accept the" link="Terms of Use" href="/terms" disabled={disabled} {...terms} />
      {!terms.error && (
        <Tooltip type="help">
          <Checkbox name="remember" label="Remember my choice" disabled={!terms.on} {...remember} />
        </Tooltip>
      )}
    </div>
  );
}

export default Terms;
