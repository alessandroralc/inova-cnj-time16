# inova-cnj-time16

## Instruções para a execução do docker-compose
1. Criar um arquivo .env na pasta docker com os propriedades abaixo:
```
FLASK_ENV= "dev"
APP_PORT= "5002"
WORKERS= "4"
THREADS= "2"
WORKER_CLASS= "gthread"
DATABASE_URL="postgres://postgres:inovacnj@127.0.0.1:5433/sanjus"
GUNICORN_CMD_ARGS= "--bind '0.0.0.0:5002' --workers 8 --worker-class gthread --threads 2 --config python:config_gunicorn"
DEBUG= "True"
prometheus_multiproc_dir= "/tmp"
METRICS_PORT= "5003"
TZ= "America/Sao_Paulo"
```
