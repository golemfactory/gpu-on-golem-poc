type useFormType = {
  value: string;
  onChange: (e: FormEvent) => void;
  error: string | undefined;
  onSubmit: (e: FormEvent) => void;
  onExample: () => void;
};
