#! /bin/bash

while inotifywait -q -e close_write /usr/local/etc/haproxy/haproxy.cfg; do
  kill -SIGUSR2 `pidof haproxy`
done
