# gpu-on-golem-poc

### Client

In the `/client` dir:

1. Install dependencies: `npm install`
2. To run the development server: `npm run dev`
3. To build an app `npm run build`
4. Serve files `npm run start`
5. For optimized static build run `npm run static`

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.


# Deployment

## Golem requestor installation

### Installation of Golem daemon and requestor
https://handbook.golem.network/requestor-tutorials/flash-tutorial-of-requestor-development


### Configure env variable
`export YAGNA_APPKEY=[yagna_key]`

You can obtain yagna key with `yagna app-key list`

## App

### Get the code
`git clone git@github.com:golemfactory/gpu-on-golem-poc.git`

### Frontend build
```shell
cd gpu-on-golem-poc/client
npm install
npm run static
rm -rf ../api/static/*
cp -R out/* ../api/static/
cd ..
```

### Backend preparations
```shell
sudo apt install redis
python3 -m venv venv
source venv/bin/activate
pip install --update pip
pip install -r api/requirements.txt
```

### Api start (can be started in `screen` or monitored by supervisor/monit/systemd):
```shell
[...]/venv/bin/uvicorn api.app:app --log-config=api/log.yml
```

This will start server on port **8000**. 

### Golem service start
```shell
[...]/venv/bin/python -m api.stable_diffusion.service
```

### Systemd services
Example files can be found in `api/systemd`.

### Env variables to control settings 
- `APP_ENV` - taken into consideration by JS code while running `npm run static` 
