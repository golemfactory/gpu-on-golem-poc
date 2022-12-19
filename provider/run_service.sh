#! /bin/bash

cd /usr/src/app
python3 service.py "$1" > out.txt 2>&1 &

