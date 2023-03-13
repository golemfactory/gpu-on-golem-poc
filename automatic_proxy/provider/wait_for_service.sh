#! /bin/bash

while ! curl -s http://localhost:"$1" > /dev/null
do
    echo waiting for service
    sleep 1
done
