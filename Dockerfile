# syntax=docker/dockerfile:1.4
FROM python:3.13.7-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN useradd -r tf2log

RUN --mount=type=cache,target=/var/cache/apk <<EOF
apk update
apk add gcc musl-dev g++ libstdc++
EOF

COPY ./requirements.txt /app/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install gunicorn redis

COPY . /app

RUN chown -R tf2log:tf2log /app/tf2log/static/css
RUN mkdir -p /app/instance
RUN apk del gcc musl-dev g++

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "tf2log:create_app()"]
CMD ["-w 4"]

USER tf2log
EXPOSE 8000
VOLUME ["/app/instance"]
