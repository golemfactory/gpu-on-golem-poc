import Image from 'next/image';
import { renderIcon } from 'assets/utils';
import { Tooltip } from 'components';

function Header() {
  return (
    <header className="absolute inset-x-0 top-[2rem] flex items-center justify-between px-[5rem] lg:top-[6rem]">
      <Image className="mx-auto lg:mx-0" src={renderIcon('logo')} alt="logo" width={88} height={64} />
      <div className="relative">
        <Tooltip type="info" text="Some useful tip" bottom />
      </div>
    </header>
  );
}

export default Header;
