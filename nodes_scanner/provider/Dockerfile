FROM maugnorbert/docker_golem_cuda_base:latest

WORKDIR /usr/src/app

#TODO: install pytorch or smth
RUN apt-get update && apt-get install -y pciutils openssh-server ufw
RUN mkdir /run/sshd
RUN echo "UseDNS no" >> /etc/ssh/sshd_config && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
