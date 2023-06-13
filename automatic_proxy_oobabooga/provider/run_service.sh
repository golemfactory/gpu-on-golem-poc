#! /bin/bash
# Znaleźć miejsce w którym odpala się oobabooga-webui

cd /home/python_user/text-generation-webui
python3 server.py --cpu --verbose --api --model facebook_opt-1.3b> out.txt 2>&1 &
