FROM python:3.11-slim

LABEL maintainer="jsribeiro123@gmail.com"

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    g++ \
    gcc \
    libpq-dev \
    libglib2.0-0 \
    libgl1 \
    libcairo2 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libxml2 \
    libxslt1.1 \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONPATH=/app/src


EXPOSE 8080

ENTRYPOINT ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
