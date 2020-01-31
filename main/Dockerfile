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
    cron

# library
RUN pip install --upgrade pip
RUN pip install \
    tweepy==3.8.0 \
    tqdm==4.36.1\
    python-dotenv==0.10.5

# copy
COPY ./src/.env /.env
COPY ./src src
COPY ./test test

# RUN git clone https://github.com/seven320/metamon_code.git

ENV USER mother
ENV HOME /home/${USER}
ENV SHELL /bin/bash


RUN echo '* * * * * python3 ./test/main.py' >> /etc/crontab
CMD ["cron", "-f"]


