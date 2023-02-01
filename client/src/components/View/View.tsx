import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import Image from 'next/image';
import { saveAs } from 'file-saver';
import { Status } from 'enums/status';
import { renderIcon } from 'assets/utils';
import { Placeholder } from 'components';
import { selectData } from 'slices/data';
import { useStatusState } from 'utils/hooks';
import url from 'utils/url';

function View({
  intermediary_image,
  value,
  blocked,
}: {
  intermediary_image?: string;
  value: string;
  blocked?: boolean;
}) {
  const data = useSelector(selectData);

  const { forState } = useStatusState();

  const [src, setSrc] = useState<string | undefined>(undefined);

  const handleImage = (src: string) => setSrc(url(src, false));

  useEffect(() => {
    !!intermediary_image && forState([Status.Processing]) && handleImage(intermediary_image);
  }, [intermediary_image, forState]);

  useEffect(() => {
    !!data?.img_url && forState([Status.Finished, Status.Blocked]) && handleImage(data?.img_url);
  }, [data?.img_url, forState]);

  const handleSave = () => !!src && saveAs(src, `${value}.jpeg`);

  return (
    <div className="relative mx-auto w-[33.2rem] md:w-[36.2rem]">
      <Placeholder>{!!src && <Image src={src} alt={value} fill />}</Placeholder>
      {!blocked && (
        <button
          className="absolute bottom-[1rem] right-[1rem] h-[2rem] w-[1.8rem] bg-black bg-center bg-no-repeat"
          style={{ backgroundImage: `url(${renderIcon('download')})` }}
          onClick={handleSave}
        />
      )}
    </div>
  );
}

export default View;
