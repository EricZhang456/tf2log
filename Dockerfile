# syntax=docker/dockerfile:1.4
FROM python:3.13.7-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install redis

COPY . /app

RUN mkdir -p /app/instance

ENTRYPOINT ["hypercorn", "-b", "0.0.0.0:8000", "tf2log:create_app()"]

EXPOSE 8000
VOLUME ["/app/instance"]
