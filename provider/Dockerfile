FROM maugnorbert/docker_golem_cuda_base:latest

WORKDIR /usr/src/app
VOLUME /usr/src/app/output

COPY service.py ./
COPY run_service.sh ./
COPY run_service_alt.sh ./
COPY generate.sh ./
COPY generate_wait.sh ./

RUN apt-get update && apt-get install -y python3-pip pciutils curl git
RUN pip install --no-cache-dir --upgrade pip wheel setuptools setuptools_rust
RUN git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
RUN pip install --no-cache-dir -r stable-diffusion-webui/requirements.txt

COPY stable-diffusion-v1-5/v1-5-pruned-emaonly.ckpt ./stable-diffusion-webui/models/Stable-diffusion
COPY openai ./stable-diffusion-webui/openai

WORKDIR stable-diffusion-webui
RUN python3 launch.py --skip-torch-cuda-test --exit
