#! /bin/bash

cd /usr/src/app/stable-diffusion-webui
python3 launch.py > out.txt 2>&1 &
