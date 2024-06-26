type useCheckboxType = {
  on: boolean;
  toggle: Noop;
  onChange: Noop;
  error?: ErrorType;
};

type CheckboxProps = {
  name: string;
  label: string;
  link?: string;
  href?: string;
  disabled: boolean;
} & useCheckboxType;
