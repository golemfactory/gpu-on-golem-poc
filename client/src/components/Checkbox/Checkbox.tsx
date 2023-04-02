import Link from 'next/link';
import { twMerge } from 'tailwind-merge';

function Checkbox({ name, label, link, href, on, onChange, disabled, error }: CheckboxProps) {
  return (
    <div className="flex min-h-[1.5rem] items-center">
      <input
        className="checkbox"
        type="checkbox"
        id={name}
        name={name}
        checked={on}
        onChange={onChange}
        disabled={disabled}
      />
      <div className="text-left">
        <label
          className={twMerge(
            'pl-[0.15rem] text-10 text-white',
            disabled ? 'text-grey hover:cursor-not-allowed' : 'hover:cursor-pointer',
          )}
          htmlFor={name}
        >
          {label}
        </label>{' '}
        {href && (
          <Link className="text-10 text-white underline" href={href}>
            {link}
          </Link>
        )}
      </div>
      {error?.length && (
        <span className="absolute left-[1.8rem] top-[1.8rem] w-[12rem] text-10 text-[#ff0000]">{error}</span>
      )}
    </div>
  );
}

export default Checkbox;
