import Link from 'next/link';
import { twMerge } from 'tailwind-merge';

function Checkbox({ name, label, link, href, on, onChange, disabled, error }: CheckboxProps) {
  return (
    <div className="flex min-h-[1.5rem] items-center">
      <input
        className="relative float-left mr-[0.6rem] h-[1.125rem] w-[1.125rem] appearance-none border-[0.125rem] border-solid border-blue bg-white outline-none before:pointer-events-none before:absolute before:h-[0.875rem] before:w-[0.875rem] before:scale-0 before:rounded-full before:bg-transparent before:opacity-0 before:content-[''] checked:border-blue checked:bg-blue checked:before:opacity-[0.16] checked:after:absolute checked:after:-mt-px checked:after:ml-[0.25rem] checked:after:block checked:after:h-[0.8125rem] checked:after:w-[0.375rem] checked:after:rotate-45 checked:after:border-[0.125rem] checked:after:border-l-0 checked:after:border-t-0 checked:after:border-solid checked:after:border-white checked:after:bg-transparent checked:after:content-[''] hover:cursor-pointer hover:before:opacity-[0.04] focus:shadow-none focus:transition-[border-color_0.2s] focus:before:scale-100 focus:before:opacity-[0.12] focus:after:absolute focus:after:z-[1] focus:after:block focus:after:h-[0.875rem] focus:after:w-[0.875rem] focus:after:rounded-[0.125rem] focus:after:bg-white focus:after:content-[''] checked:focus:border-blue checked:focus:bg-blue checked:focus:before:scale-100 checked:focus:after:-mt-px checked:focus:after:ml-[0.25rem] checked:focus:after:h-[0.8125rem] checked:focus:after:w-[0.375rem] checked:focus:after:rotate-45 checked:focus:after:rounded-none checked:focus:after:border-[0.125rem] checked:focus:after:border-l-0 checked:focus:after:border-t-0 checked:focus:after:border-solid checked:focus:after:border-white checked:focus:after:bg-blue disabled:cursor-not-allowed disabled:border-grey disabled:bg-grey"
        type="checkbox"
        id={name}
        name={name}
        checked={on}
        onChange={onChange}
        disabled={disabled}
      />
      <div className="text-left text-[12px] font-light uppercase">
        <label
          className={twMerge('pl-[0.15rem]', disabled ? 'opacity-75 hover:cursor-not-allowed' : 'hover:cursor-pointer')}
          htmlFor={name}
        >
          {label}
        </label>{' '}
        {href && (
          <Link className="underline" href={href}>
            {link}
          </Link>
        )}
      </div>
      {error?.length && (
        <span className="absolute left-[1.8rem] top-[1.8rem] w-[12rem] text-[10px] font-light text-[#ff0000]">
          {error}
        </span>
      )}
    </div>
  );
}

export default Checkbox;
