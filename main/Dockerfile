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

# library
RUN pip install --upgrade pip
RUN pip install \
    tweepy==3.8.0 \
    tqdm==4.36.1\
    pykakasi==1.2\
    python-dotenv==1.0.0\
    pytest==5.4.1\
    pytest-mock==3.1.0

# RUN service cron start
# RUN git clone https://github.com/seven320/metamon_code.git
COPY ./src src
COPY ./tests tests
COPY ./images images
COPY ./env env
COPY ./crontab /var/spool/cron/crontabs/root
CMD ["busybox", "crond", "-l", "2", "-L", "/dev/stderr", "-f"]

ENV USER mother
ENV HOME /home/${USER}
ENV SHELL /bin/sh