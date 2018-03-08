FROM python:3.6.3-alpine3.7

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV FUNNEL_API_CONFIG "/secrets/server-config.yaml"

## Copy app files
COPY server ./server

## Start app
CMD gunicorn -w 3 -b 0.0.0.0:8080 'server:create_app()'
