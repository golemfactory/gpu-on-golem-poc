#! /bin/bash

echo "pod started"

if [[ $PUBLIC_KEY ]]
then
    mkdir -p ~/.ssh
    chmod 700 ~/.ssh
    cd ~/.ssh
    echo $PUBLIC_KEY >> authorized_keys
    chmod 700 -R ~/.ssh
    cd /
    service ssh start
fi

cd /usr/src/app/stable-diffusion-webui
python3 launch.py --server-name 0.0.0.0 --port 8000 --api --xformers > out.txt 2>&1
