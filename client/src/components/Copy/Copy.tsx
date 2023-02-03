import { useState } from 'react';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { renderIcon } from 'assets/utils';

function Copy({ value }: { value: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => setCopied(true);

  const sharedStyles = 'absolute right-[0.4rem] md:-right-[1.2rem] top-0 h-[1.8rem] w-[1.8rem] bg-center bg-no-repeat';

  return copied ? (
    <div className={sharedStyles + ' cursor-default'} style={{ backgroundImage: `url(${renderIcon('checkmark')})` }} />
  ) : (
    <CopyToClipboard text={value} onCopy={handleCopy}>
      <div className={sharedStyles + ' cursor-pointer'} style={{ backgroundImage: `url(${renderIcon('copy')})` }} />
    </CopyToClipboard>
  );
}

export default Copy;
