FROM python:3.11

# provide default user and group id in case these are not passed through --build-arg
ARG UID=1000
ARG GID=1000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y  \
    postgresql-client libpq-dev  \
    ntp \
    less \
    --no-install-recommends && apt-get clean

RUN pip install --upgrade pip

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY rent_golem /code/

RUN addgroup --gid $GID --system dev
RUN useradd --uid=${UID} --gid=${GID} --shell /bin/bash dev
RUN chown -R dev:dev /code

USER dev
