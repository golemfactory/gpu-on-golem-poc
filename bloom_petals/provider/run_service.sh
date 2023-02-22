#! /bin/bash

cd /usr/src/app
python -m petals.cli.run_server test-bloomd-6b3 --num_blocks 30 --initial_peers "$1" > out.txt 2>&1 &
