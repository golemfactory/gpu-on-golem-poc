type useFormType = {
  example: string;
  value: string;
  onChange: (e: FormEvent) => void;
  error: string | undefined;
  onSubmit: (e: FormEvent) => void;
  onReset?: () => void;
};
