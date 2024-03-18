import { useCopyToClipboard } from 'react-use';
import { renderIcon } from 'assets/utils';

function Copy({ value }: { value: string }) {
  const [copy, copyToClipboard] = useCopyToClipboard();

  const handleCopy = () => copyToClipboard(value);

  const sharedStyles =
    'bg-transparent absolute right-2.5 top-2.5 h-[1.8rem] w-[1.8rem] border-none bg-center bg-no-repeat';

  return copy.value ? (
    <div className={sharedStyles} style={{ backgroundImage: `url(${renderIcon('checkmark')})` }} />
  ) : (
    <button onClick={handleCopy} className={sharedStyles} style={{ backgroundImage: `url(${renderIcon('copy')})` }} />
  );
}

export default Copy;
