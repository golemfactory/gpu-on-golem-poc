const url = (path: string, ws: boolean, id?: string) =>
  `${ws ? 'wss' : 'https'}://${process.env.NEXT_PUBLIC_HOSTNAME}/${path}${ws ? '/ws' : ''}/${id ? id + (ws ? '/' : '') : ''}`;

export default url;
