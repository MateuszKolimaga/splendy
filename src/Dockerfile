FROM python:3.12
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY ./requirements/base.txt .
COPY ./requirements/local.txt .
RUN pip install -r local.txt