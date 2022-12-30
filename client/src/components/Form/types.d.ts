type useFormType = {
  value: string;
  onChange: (e: FormEvent) => void;
  error: string | undefined;
  disabled: boolean;
  onSubmit: (e: FormEvent) => void;
  onExample: () => void;
  onClear: () => void;
};
