FROM maugnorbert/docker_golem_cuda_base:latest

WORKDIR /usr/src/app
VOLUME /usr/src/app/output

COPY run_service.sh ./
COPY wait_for_service.sh ./
#COPY proxy.conf /etc/nginx/conf.d/


RUN apt-get update && apt-get install -y python3-pip pciutils jq \
  make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev\
  libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl\
  git

RUN useradd -m python_user

WORKDIR /home/python_user
USER python_user

RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv

ENV HOME  /home/python_user
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

RUN pyenv install 3.10.9
RUN pyenv global 3.10.9

RUN #python3 -V

RUN git clone https://github.com/oobabooga/text-generation-webui

RUN pip install torch torchvision torchaudio # tqdm gradio_client==0.2.5 gradio==3.31.0

RUN cd text-generation-webui && pip install -r requirements.txt


RUN cd text-generation-webui && python3 download-model.py facebook/opt-1.3b
RUN #pwd
RUN #cd text-generation-webui/prompts && ls -la
RUN #cat /home/python_user/text-generation-webui/prompts/QA.txt

#RUN cd text-generation-webui && python3 server.py --cpu --verbose
RUN #bash /usr/src/app/run_service.sh

#RUN bash /usr/src/app/wait_for_service.sh
RUN #sleep 10
RUN #curl http://localhost:5000/api/v1/generate --data '{"prompt": "I am happy prompt and I", , "max_new_tokens, ": 250, , "do_sample, ": True, , "temperature, ": 1.3, , "top_p, ": 0.1, , "typical_p, ": 1, , "epsilon_cutoff, ": 0, , "eta_cutoff, ": 0, , "tfs, ": 1, , "top_a, ": 0, , "repetition_penalty, ": 1.18, , "top_k, ": 40, , "min_length, ": 0, , "no_repeat_ngram_size, ": 0, , "num_beams, ": 1, , "penalty_alpha, ": 0, , "length_penalty, ": 1, , "early_stopping, ": False, , "mirostat_mode, ": 0, , "mirostat_tau, ": 5, , "mirostat_eta, ": 0.1, , "seed, ": -1, , "add_bos_token, ": True, , "truncation_length, ": 2048, , "ban_eos_token, ": False, , "skip_special_tokens, ": True, , "stopping_strings, ": []}'

CMD echo "Dockerfile automatic proxy oobabooga-webui have started working."

#RUN apt-get update && apt-get install -y python3-pip pciutils curl git net-tools nginx
#RUN pip install --no-cache-dir --upgrade pip wheel setuptools setuptools_rust
##RUN git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
#RUN git clone -b patch-1 https://github.com/wk5ovc/stable-diffusion-webui.git
#RUN pip install --no-cache-dir -r stable-diffusion-webui/requirements.txt

#ENV TORCH_CUDA_ARCH_LIST=6.0;6.1;6.2;7.0;7.2;7.5;8.0;8.6
#RUN pip install xformers==0.0.20
#
#COPY stable-diffusion-v1-5/v1-5-pruned-emaonly.ckpt ./stable-diffusion-webui/models/Stable-diffusion
#COPY openai ./stable-diffusion-webui/openai
#
#RUN rm /etc/nginx/sites-enabled/default
#
#WORKDIR stable-diffusion-webui
#
## Disabling Gzipped responses from API
#RUN sed -i '/app.add_middleware(GZipMiddleware, minimum_size=1000)/d' webui.py
#
## Run once and exit to download and setup dependencies
#RUN python3 launch.py --skip-torch-cuda-test --exit
#RUN python3 -c 'from modules.deepbooru import model; model.load()'
#RUN python3 -c 'from modules.codeformer_model import setup_model; setup_model(None)'
#RUN python3 -c 'from modules.gfpgan_model import gfpgann; gfpgann()'
#RUN python3 -c 'from modules.shared import interrogator; interrogator.load()'
