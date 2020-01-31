FROM python:3.7

MAINTAINER Ken Kato <github: seven320>

RUN apt-get update && \
    apt-get install -y \
    curl \
    tmux \
    git \
    make \
    vim

# library
RUN pip install --upgrade pip
RUN pip install \
    tweepy==3.8.0 \
    tqdm==4.36.1\
    python-dotenv==0.10.5

ENV USER mother
ENV HOME /home/${USER}
ENV SHELL /bin/bash


