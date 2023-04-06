const url = (path: string, ws: boolean, id?: string) =>{
    let url = `${ws ? 'wss' : 'https'}://${process.env.NEXT_PUBLIC_HOSTNAME}/${path}${ws ? '/ws' : ''}/${id ? id + '/' : ''}`;
    return !ws && url.endsWith('/') ? url.slice(0, -1) : url;
}


export default url;
