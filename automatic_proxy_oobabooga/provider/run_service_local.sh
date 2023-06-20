#! /bin/bash
# Znaleźć miejsce w którym odpala się oobabooga-webui

cd /home/python_user/text-generation-webui
python3 server.py --cpu --verbose --api --api-blocking-port "$1" --listen-host "$2" --listen-port "$3" --model facebook_opt-1.3b > /usr/src/app/output/out.txt 2>&1 &
