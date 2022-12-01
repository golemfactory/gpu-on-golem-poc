#! /bin/bash

cd /usr/src/app
python3 service.py > out.txt 2>&1 &
#flask --app service run &
