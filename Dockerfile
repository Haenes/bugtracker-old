# syntax=docker/dockerfile:1

FROM python:3.10.12-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt entrypoint.sh ./

RUN apk update && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del build-deps

COPY . .

ENTRYPOINT ["sh", "entrypoint.sh"]
