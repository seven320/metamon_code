FROM python:3.7

MAINTAINER KenKato <github: seven320>

RUN cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN apt-get update && \
    apt-get install -y \
    curl \
    tmux \
    git \
    make \
    vim \
    tree \
    cron \
    busybox-static

# library
RUN pip install --upgrade pip
RUN pip install \
    tweepy==3.8.0 \
    tqdm==4.36.1\
    python-dotenv==0.10.5

# RUN service cron start
RUN git clone -b dev https://github.com/seven320/metamon_code.git
COPY ./src/.env ./metamon_code/main/src/.env
RUN mv ./metamon_code/main/crontab /var/spool/cron/crontabs/root
CMD busybox crond -l 2 -L /dev/stderr -f

ENV USER mother
ENV HOME /home/${USER}
ENV SHELL /bin/bash