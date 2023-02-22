FROM maugnorbert/docker_golem_cuda_base:latest

WORKDIR /usr/src/app
VOLUME /usr/src/app/output

COPY run_service.sh ./
COPY requirements.txt ./

RUN apt-get update && apt-get install -y python3-pip pciutils curl git net-tools
RUN pip install --no-cache-dir --upgrade pip wheel setuptools setuptools_rust
RUN pip install --no-cache-dir -r requirements.txt

COPY test-bloomd-6b3 ./test-bloomd-6b3
