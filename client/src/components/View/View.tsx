import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { useToggle } from 'react-use';
import Image from 'next/image';
import Link from 'next/link';
import { Dialog } from '@headlessui/react';
import { saveAs } from 'file-saver';
import { Status } from 'enums/status';
import { renderIcon } from 'assets/utils';
import { Locked, Placeholder, useLocked } from 'components';
import { selectData } from 'slices/data';
import { useStatusState } from 'utils/hooks';
import url from 'utils/url';

function View({
  intermediary_image,
  value,
  blocked,
  onReset,
}: {
  intermediary_image?: string;
  value: string;
  blocked?: boolean;
  onReset?: Noop;
}) {
  const { limited, locked, count, until, onUpdate } = useLocked();

  const data = useSelector(selectData);

  const { forState } = useStatusState();

  const [src, setSrc] = useState<string | undefined>(undefined);
  const [preview, onTogglePreview] = useToggle(false);

  useEffect(() => {
    !!data.image && forState([Status.Finished]) && handleImage(data.image);
  }, [data.image, forState]);

  useEffect(() => {
    !value && data.image && !!src && onTogglePreview();
  }, [value, data.image, src]);

  const handleImage = (src: string) => setSrc(url(src, false));

  useEffect(() => {
    !!intermediary_image && forState([Status.Processing]) && handleImage(intermediary_image);
  }, [intermediary_image, forState]);

  useEffect(() => {
    !!data?.img_url && forState([Status.Finished, Status.Blocked]) && handleImage(data?.img_url);
  }, [data?.img_url, forState]);

  const handleSave = () => !!src && saveAs(src, `${value}.jpeg`);

  const disabled = forState([Status.Processing]);

  useEffect(() => {
    if (locked && !intermediary_image && !!src && value) {
      if (!count) {
        onUpdate(Date.now() + parseFloat(process.env.NEXT_PUBLIC_LOCK_TIME_IN_SEC!) * 1000, 1);
      } else {
        onUpdate(until!, count + 1);
      }
    }
  }, [locked, intermediary_image, src]);

  const total = Number(process.env.NEXT_PUBLIC_LOCK_COUNT);

  const text = 'Check out my artwork created with the Golem AI Image Generator!';
  const hashtags = ['GolemNetwork $GLM', 'AI'];

  const handleOpen = () =>
    window.open(
      `https://twitter.com/intent/post?text=${text}&url=${window.location.href}images/${data.job_id}&hashtags=${hashtags}`,
    );

  return (
    <>
      <div className="flex flex-col gap-8 md:flex-row">
        <div className="relative mx-auto w-[288px] bg-white p-[1.6rem]">
          <Placeholder>
            {!intermediary_image && !src ? (
              <div className="h-full w-full bg-grey motion-safe:animate-pulse" />
            ) : (
              !!src && <Image src={src} alt={value} fill className="cursor-pointer" onClick={onTogglePreview} />
            )}
          </Placeholder>
        </div>
        <div className="flex flex-col items-center justify-end gap-10">
          <div className="flex flex-col items-center gap-4">
            {!value && !limited ? (
              <Link
                className="flex h-[44px] w-[288px] flex-col items-center justify-center border-[1px] border-solid border-blue bg-blue font-sans text-[12px] font-semibold uppercase leading-[1.2] tracking-[2px] text-white hover:bg-transparent hover:text-blue md:w-[215px]"
                href="/"
                onClick={onReset}
              >
                Check it out
              </Link>
            ) : (
              <button
                className="flex h-[44px] w-[288px] flex-col items-center justify-center bg-blue text-[12px] leading-[1.2] tracking-[2px] disabled:border-grey disabled:bg-grey disabled:text-black md:w-[215px]"
                onClick={onReset}
                disabled={disabled || limited}
              >
                Try again
                {!disabled && Boolean(count) && count !== total && (
                  <span>
                    ({total - count!} of {total} left)
                  </span>
                )}
                {limited && <Locked until={until!} onUpdate={onUpdate} />}
              </button>
            )}
          </div>
          {!blocked && (
            <div className="flex flex-col gap-2">
              <button
                className="flex w-[288px] items-center justify-center bg-white p-[12px] text-[12px] tracking-[2px] text-blue disabled:border-grey disabled:bg-white disabled:text-stone md:w-[215px]"
                onClick={handleSave}
                disabled={disabled}
              >
                <Image
                  className="mr-4"
                  src={renderIcon(disabled ? 'downloadStone' : 'download')}
                  alt="download image"
                  width={12}
                  height={12}
                />
                Download Image
              </button>
              <div className="flex w-[288px] justify-between font-light md:w-[215px]">
                <span>Resolution</span>
                <span>1024x1024</span>
              </div>
            </div>
          )}
          {!!src && forState([Status.Finished]) ? (
            <button
              className="flex w-[288px] items-center justify-center bg-white p-[12px] text-[12px] tracking-[2px] text-blue md:w-[215px]"
              onClick={handleOpen}
            >
              Share on X
            </button>
          ) : (
            <div className="h-[44px]" />
          )}
        </div>
      </div>
      <Dialog open={preview} onClose={onTogglePreview} className="relative z-50">
        <div className="fixed inset-0 bg-black bg-opacity-80">
          <Dialog.Panel>
            <Image
              src={src!}
              alt={value}
              fill
              className="!inset-1/2 !h-auto -translate-x-1/2 -translate-y-2/3 transform p-[1.6rem] md:!h-full md:!w-auto md:-translate-y-1/2 md:p-[10.6rem]"
            />
          </Dialog.Panel>
        </div>
      </Dialog>
    </>
  );
}

export default View;
