FROM maugnorbert/docker_golem_cuda_base:latest

WORKDIR /usr/src/app
VOLUME /usr/src/app/output

COPY run_service.sh ./
COPY wait_for_service.sh ./
COPY proxy.conf /etc/nginx/conf.d/

RUN apt-get update && apt-get install -y python3-pip pciutils jq \
  make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev\
  libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl\
  git nginx

RUN rm /etc/nginx/sites-enabled/default

RUN useradd -m python_user
WORKDIR /home/python_user
USER python_user

RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv

ENV HOME  /home/python_user
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

RUN pyenv install 3.10.9
RUN pyenv global 3.10.9

RUN git clone https://github.com/oobabooga/text-generation-webui
COPY MedQuAD_output.json text-generation-webui/training/datasets/

RUN pip install torch torchvision torchaudio
RUN cd text-generation-webui && pip install -r requirements.txt

RUN cd text-generation-webui && python3 download-model.py facebook/opt-1.3b
