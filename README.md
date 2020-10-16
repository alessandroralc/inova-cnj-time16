# inova-cnj-time16

## Instruções para a execução do docker-compose
1. Criar um arquivo .env na pasta docker com os propriedades abaixo:
```
FLASK_ENV=dev
APP_PORT=5002
WORKERS=4
THREADS=2
WORKER_CLASS=gthread
DATABASE_URL=postgres://sanjus_app:xxxxxx@127.0.0.1:5433/sanjus
GUNICORN_CMD_ARGS=--bind '0.0.0.0:5002' --workers 8 --worker-class gthread --threads 2 --config python:config_gunicorn
DEBUG=True
prometheus_multiproc_dir=/tmp
METRICS_PORT=5003
TZ=America/Sao_Paulo
```
2. Automaticamente o container (sanjus_init) irá executar as migrations do banco de dados, abaixo detalhamos alguns comandos que podem ser utilizados para a geração automatizada de migrations.

Caso seja alterada alguma entidade do módulo src.entidades é necessário executar o alembic para que uma nova migration seja gerada para isso, deve-se acessar a pasta do projeto e executar o comando: `python manage.py db migrate`.
Após a execução do `migrate` será criado um novo arquivo .py dentro de migrations/versions. É recomendável a validação e atualização do arquivo antes de efetivar a migration. Para efetivar a migration o seguinte comando pode ser utilizado `python manage.py db upgrade`
Também é possível realizar downgrade e outros tipos de atualização conforme detalhamento [Documentação Alembic](https://alembic.sqlalchemy.org/en/latest/)

