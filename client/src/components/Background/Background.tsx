import backgroundPNG from 'assets/background.png';

function Background() {
  const style = {
    style: { backgroundImage: `url(${backgroundPNG.src})` },
  };

  return (
    <div className="absolute inset-0 -z-10 columns-2">
      <div className="background" {...style} />
      <div className="background -scale-x-100" {...style} />
    </div>
  );
}

export default Background;
