FROM python:3.12-slim

MAINTAINER SwA <swojak.a@gmail.com>

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.4.2 \
    PYTHONDONTWRITEBYTECODE=0 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Europe/Warsaw

ENV PACKAGES="\
    apt-utils \
    bash \
    ca-certificates \
    curl \
    dnsutils \
    gettext \
    git \
    gnupg2 \
    gdal-bin \
    iputils-ping \
    less \
    locales \
    make \
    nano \
    netcat-traditional \
    postgresql-client \
    screen \
    software-properties-common \
    ssh \
    sudo \
    syslinux \
    tar \
    telnet \
    tzdata \
    udev \
    vim \
    wget \
    zip \
    "

RUN mkdir -p /backend

SHELL ["/bin/bash", "-c"]

WORKDIR /backend

RUN echo $TZ > /etc/timezone && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    apt-get update && \
    apt-get install -y -f --no-install-recommends $PACKAGES && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen && \
    apt-get autoremove --purge -y && \
    rm -rf /root/.cache/ && \
    rm -rf /usr/src/ && \
    rm -rf /var/lib/apt/lists/*

COPY docker/scripts/install-poetry.py /install-poetry.py
RUN python /install-poetry.py --version $POETRY_VERSION && \
    echo $HOME && \
    ln -s $HOME/.local/bin/poetry /usr/bin/poetry && \
    poetry config virtualenvs.create false

COPY backend/pyproject.toml /backend/pyproject.toml
COPY backend/poetry.lock /backend/poetry.lock
COPY docker/scripts /scripts
COPY docker/config/nginx /etc/nginx/sites-available/
COPY docker/config/nginx.conf /etc/nginx/nginx.conf

RUN apt-get update \
    && apt-get install libev-dev libevdev2 g++ -y\
    && poetry install \
    && apt-get remove g++ -y

COPY backend /backend

COPY .build-environment /

RUN source /.build-environment && \
    rm -rf /.build-environment && \
    ./manage.py compilemessages && \
    ./manage.py collectstatic --noinput

COPY docker/docker-entrypoint /docker-entrypoint

ENTRYPOINT ["/docker-entrypoint"]
