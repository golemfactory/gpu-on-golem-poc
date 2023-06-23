#! /bin/bash

while ! curl -s http://localhost:"$1"/api/v1/generate --data '{"prompt": "I am happy prompt and I", "max_new_tokens": 5}' > /dev/null
do
    echo waiting for service
    sleep 1
done
echo Service worked
