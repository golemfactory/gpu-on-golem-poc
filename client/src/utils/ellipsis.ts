const ellipsis = (address: string, chars = 10) => {
  const ellipsis = '...';

  const startIndex = Math.floor(chars / 2) + 2;
  const endIndex = address.length - Math.floor(chars / 2) - 2;

  return `${address.slice(0, startIndex)}${ellipsis}${address.slice(endIndex)}`;
};

export default ellipsis;
