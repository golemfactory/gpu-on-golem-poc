# gpu-on-golem-poc

When server is running behind proxy eg. your Apache conf has
```
...
ProxyPass "/sd" "http://localhost:8000"
ProxyPassReverse "/sd" "http://localhost:8000"
...
```
you should start it with `uvicorn app:app --root-path /sd`.

