FROM python:3.6

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

# copy
# COPY ./src/.env /.env
# COPY ./src src
# COPY ./test test
# COPY crontab /var/spool/cron/crontabs/root



# RUN echo '* * * * * root python3 ./test/main.py' >> /etc/cron.d/10min
# RUN service cron start
RUN git clone -b dev https://github.com/seven320/metamon_code.git
CMD busybox crond -l 2 -L /dev/stderr -f

ENV USER mother
ENV HOME /home/${USER}
ENV SHELL /bin/bash




