import empty from 'utils/empty';

const encodeQuery = (key: string, value: string) =>
  process.env.NODE_ENV === 'development'
    ? `&${key}=${value}`
    : `&${encodeURIComponent(key)}=${encodeURIComponent(value)}`;

export const queryBuild = (params: object) => {
  let query = '';

  Object.entries(params).forEach(([key, value]: [string, string | string[]]) => {
    if (!empty(value)) {
      query += encodeQuery(key, Array.isArray(value) ? value.join(',') : value);
    }
  });

  return query.replace('&', '');
};

export default queryBuild;
