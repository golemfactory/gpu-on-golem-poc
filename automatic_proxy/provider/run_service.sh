#! /bin/bash

cd /usr/src/app/stable-diffusion-webui
python3 launch.py --server-name "$1" --port "$2" > out.txt 2>&1 &
