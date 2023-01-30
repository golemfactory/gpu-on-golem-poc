#!/bin/bash

# Acquire exclusive lock (wait 3 seconds) and print status.json contents to stdout.

cd /usr/src/app
flock -x -w 3 output/status.lock cat output/status.json
