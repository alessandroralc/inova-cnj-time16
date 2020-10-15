# inova-cnj-time16

## Instruções para a execução do docker-compose
1. Criar um arquivo .env na pasta docker com os propriedades abaixo:
```
FLASK_ENV= "dev"
APP_PORT= "5002"
WORKERS= "4"
THREADS= "2"
WORKER_CLASS= "gthread"
POSTGRES_HOST= "127.0.0.1"
POSTGRES_PORT= "5433"
POSTGRES_DATABASE= "sanjus"
POSTGRES_USERNAME= "postgres"
POSTGRES_PASS= "inovacnj"
GUNICORN_CMD_ARGS= "--bind '0.0.0.0:5002' --workers 8 --worker-class gthread --threads 2 --config python:config_gunicorn"
DEBUG= "True"
prometheus_multiproc_dir= "/tmp"
METRICS_PORT= "5003"
TZ= "America/Sao_Paulo"
```
