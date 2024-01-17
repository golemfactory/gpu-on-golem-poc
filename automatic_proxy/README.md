# Automatic1111 proxy on Golem
Lets you use run stable diffusion webui from Automatic1111 on Golem provider via LocalProxy.

## Provider
### Build
- You need to first build `maugnorbert/docker_golem_cuda_base` image to be able to build stable diffusion provider image.
- You need to download stable-diffusion model files (`stable-diffusion-v1-5`).
- You need to have openai directory and clip-vit-large-patch14 repository inside 

### Runpod build
To create image suitable to run on Runpod.io build it with runpod.Dockefile and send to public docker registry.

Exemplary build command: `docker build -t automatic/sd:latest -f runpod.Dockerfile .`

#### "Secure cloud" instance details:

Docker image name: [your_image_public_name_and-tag] e.g. `stan7123/automatic-sd`

Docker script: `bash -c '/usr/src/app/start.sh'`

Expose HTTP ports: `8000`

Expose TCP ports: `22`

Container disk and volume disk: `20GB`


## Requestor
Create venv based on api/requirements.txt

Then from venv:
```
cd ..
python -m automatic_proxy.requestor.service
```
