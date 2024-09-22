# syntax=docker/dockerfile:1

FROM python:3.12-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN addgroup nonroot && \
    adduser \
        --disabled-password \
        --ingroup nonroot \
        user && \
    chown -R user:nonroot \
        /usr/local/lib/python3.12/site-packages/django/contrib/auth/migrations && \
    mkdir /home/user/static/ && \
    chown -R user:nonroot /home/user/static/

USER user

COPY . .
