# Rent GPU app

App is working as requestor in Golem network easing access to providers by proxying traffic.
Providers can serve different packages which can be added as kind of modules.

## How to setup

### Packages

Packages (Golem provider images) are located in different directories:
- PyTorch + SSH -> `rent_gpu/provider/ssh`
- JupyterLab -> `rent_gpu/provider/jupyter`
- Stable diffusion webUI with stable diffusion 1.5 model -> `automatic_proxy/provider` 
- Text webUI + facebook/opt-1.3b model -> `text_webui_proxy/provider`

To build an image:
- `docker build -t [image_tag] .`
- `gvmkit-build [image_tag]` -> this builds and image which you must place under publicly accessible URL + `sha3sum -a 224 [gvmi_image_file]` 

or 

- You can use newest registy.golem.network service and new version of gvmkit-build: `gvmkit-build [image_tag] --push-to [username]/[repository]:[tag]` -> This will create package from docker image, send it to registry from which you can host the image. For details see registry.golem.network API.

### BE

1. Install Golem as requestor -> https://handbook.golem.network/requestor-tutorials/flash-tutorial-of-requestor-development
2. Install Redis
3. Create virtual env and install `rent_gpu/requestor/requirements.txt`.
4. From virtual env run:
    - `python -m rent_gpu/requestor/db` -> preparing DB
    - `python -m rent_gpu/requestor/scanner [subnet]` -> Scanning for GPU providers. Current subnet with GPU providers is `gpu-test`
    - `uvicorn rent_gpu.requestor.api.app:app` -> Running webserver with API.
    - set env variable `export YAGNA_APPKEY=[app_key]`
    - set env variable `export YAGNA_PAYMENT_NETWORK=goerli` -> assuming that you used goerli faucet 
    - `rq worker` -> Running jobs worker. One worker can handle only one rented provider.

### FE

If BE is running, just go to http://localhost:8000
