import { useState } from 'react';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { renderIcon } from 'assets/utils';

function Copy({ value }: { value: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => setCopied(true);

  return copied ? (
    <div
      className="mx-auto mb-[1.2rem] w-[7.4rem] cursor-default bg-left bg-no-repeat text-9 text-stone"
      style={{ backgroundImage: `url(${renderIcon('checkmark')})` }}
    >
      Copied
    </div>
  ) : (
    <CopyToClipboard text={value} onCopy={handleCopy}>
      <div
        className="mx-auto mb-[1.2rem] w-[14rem] cursor-pointer bg-left bg-no-repeat text-9 text-stone underline"
        style={{ backgroundImage: `url(${renderIcon('copy')})` }}
      >
        Copy to clipboard
      </div>
    </CopyToClipboard>
  );
}

export default Copy;
