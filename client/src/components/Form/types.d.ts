type FormEventType = (e: FormEvent) => void;

type ErrorType = string | undefined;

type onErrorType = (error?: ErrorType) => void;

type useErrorType = {
  error: ErrorType;
  onError: onErrorType;
};

type useFormType = {
  value: string;
  onChange: FormEventType;
  error: ErrorType;
  disabled: boolean;
  onSubmit: FormEventType;
  onExample: Noop;
  onClear: Noop;
  terms: useTermsType;
};
