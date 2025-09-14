# syntax=docker/dockerfile:1.4
FROM python:3.13.7-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN <<EOF
apk update
apk add gcc musl-dev g++ libstdc++
EOF

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn redis

COPY . /app

RUN mkdir -p /app/instance
RUN apk del gcc musl-dev g++

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "tf2log:create_app()"]
CMD ["-w 4"]

EXPOSE 8000
VOLUME ["/app/instance"]
