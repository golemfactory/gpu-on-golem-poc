# gpu-on-golem-poc

When server is running behind proxy eg. your Apache conf has

```
...
ProxyPass "/sd" "http://localhost:8000"
ProxyPassReverse "/sd" "http://localhost:8000"
...
```

you should start it with `uvicorn app:app --root-path /sd`.

### Client

In the `/client` dir:

1. Install dependencies: `npm install`
2. To run the development server: `npm run dev`
3. To build an app `npm run build`
4. Serve files `npm run start`
5. For optimized static build run `npm run static`

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.
