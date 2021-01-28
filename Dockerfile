FROM python:3.8.5-alpine

ENV PYTHONUNBUFFERED = 1

# RUN apt-get update && apt-get install -y git
RUN apk update && apk add --no-cache \
    curl-dev \
    gcc \
    git \
    vim

RUN  pip install --upgrade pip

WORKDIR /app

ADD . /app

COPY  ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY  . /app

ENTRYPOINT ["sh", "entrypoint.sh"]
