FROM haproxy

USER root
RUN set -eux; \
    apt-get update && apt-get install -y --no-install-recommends inotify-tools

USER haproxy
