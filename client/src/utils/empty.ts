const empty = (value: undefined | null | number | object | string): boolean =>
  value === undefined ||
  value === null ||
  (typeof value === 'number' && isNaN(value)) ||
  (typeof value === 'object' && Object.keys(value).length === 0) ||
  (typeof value === 'string' && value.trim().length === 0);

export default empty;
