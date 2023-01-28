function gaEvent(action: string, params: object) {
  // @ts-ignore
  window.gtag('event', action, params);
}

export default gaEvent;
