FROM nvidia/cuda:12.3.1-base-ubuntu22.04

WORKDIR /usr/src/app
VOLUME /usr/src/app/output

COPY stable-diffusion-xl-base-1.0 ./stable-diffusion-xl-base-1.0
COPY sdxl_lightning_4step_unet.safetensors ./
COPY requirements.txt ./
COPY worker.py ./
COPY service.py ./
COPY run_task.sh ./
COPY run_service.sh ./
COPY generate.sh ./
COPY generate_wait.sh ./
COPY get_status.sh ./

RUN apt-get update && apt-get install -y python3-pip pciutils
RUN pip install --no-cache-dir --upgrade pip wheel setuptools setuptools_rust
RUN pip install --no-cache-dir -r requirements.txt
