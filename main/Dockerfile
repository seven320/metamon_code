FROM python:3.8-alpine

RUN apk update && \
    apk --no-cache add \
    curl \
    tmux \
    git \
    make \
    vim \
    tree \
    busybox-static

WORKDIR /app

# library
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"
ENV UV_SYSTEM_PYTHON=1

COPY ./requirements.txt /tmp/requirements.txt
RUN uv pip install --no-cache -r /tmp/requirements.txt

COPY ./src ./src
COPY ./tests ./tests
COPY ./images ./images
COPY ./env ./env
COPY ./crontab /var/spool/cron/crontabs/root
CMD ["busybox", "crond", "-l", "2", "-L", "/dev/stderr", "-f"]

ENV USER mother
ENV HOME /home/${USER}
ENV SHELL /bin/sh
