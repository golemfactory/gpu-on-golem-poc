FROM maugnorbert/docker_golem_cuda_base:latest

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt-get update && apt-get install -y python3-pip pciutils openssh-server ufw
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /run/sshd
RUN echo "UseDNS no" >> /etc/ssh/sshd_config && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
