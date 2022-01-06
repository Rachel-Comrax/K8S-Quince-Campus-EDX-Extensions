FROM python:3.8-slim as base-image

ENV PYTHONUNBUFFERED 1
RUN apt update -y && apt install make

FROM base-image as test-image

WORKDIR /app

COPY requirements/test.txt requirements/test.txt
RUN pip install -r requirements/test.txt
