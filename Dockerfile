FROM python:3.8

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV IN_OPEN_DOCKER 1

RUN apt update && apt install -y \
    postgresql-client

COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv && pipenv install --system

COPY . .

EXPOSE 8005