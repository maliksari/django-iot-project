FROM python:3.9-slim AS iot-app

WORKDIR /iot-app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY ./.env .
RUN pip install -r requirements.txt

COPY . /iot-app

CMD ["python", "tcp_server.py"]

EXPOSE 9999