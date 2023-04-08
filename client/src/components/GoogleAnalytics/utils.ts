export function gaEvent(action: string, params: object) {
  window.gtag('event', action, params);
}
