FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt -qq -y install git curl python3 python3-venv python3-pip

RUN mkdir -p $HOME/.local/share/ya-installer/terms
RUN touch $HOME/.local/share/ya-installer/terms/testnet-01.tag
RUN curl -sSf https://join.golem.network/as-requestor | bash - || echo "Nothing to see here"
ENV PATH=${PATH}:/root/.local/bin/:/root/.local/
