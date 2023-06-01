FROM python:3.11.3

COPY . /usr/local/src
WORKDIR /usr/local/src

RUN apt-get update \
    && apt-get install -y systemctl cron vim git \
    && systemctl start cron

RUN git config --global user.name masakazu-hirano \
    && git config --global user.email @users.noreply.github.com

RUN pip install --upgrade pip \
    && pip install -r requirements.txt
