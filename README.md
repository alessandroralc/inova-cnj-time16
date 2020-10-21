# inova-cnj-time16

## Definições negociais

## Arquitetura da solução

![Arquitura do Sistema](doc/arquitetura.png)

### Armazenamento

#### ElasticSearch

Utilizado como base de dados NoSQL analítica. Os dados brutos dos arquivos jsons do DataJud são indexados. O dashboard contruído é exibido diretamente na aplicação. A carga da prova de conceito foi realizada com os dados disponibilizados pelo desafio.

- O dashboard foi construído com o Kibana e permite que os usuários visualizem de forma integrada a nossa aplicação as informações do seu acervo.

##### Licenciamento:

- ElasticSearch: Apache License 2.0
- Docker: Apache License 2.0

#### PostreSQL

Utilizado para dar estrutura das tabelas que suportam a lógica da aplicação. Os dados do DataJud são transformados para estrutura relacional diretamenta da base do ElasticSearch.

- O ETL importa os dados básicos do processo e a movimentação. São esses movimentos que são validados sistema.
- Ambos os componentes são instanciados e carregados com containers Dockers. Toda carga de dados e ETL é realizado automaticamente com scripts de build do sistema.

##### Licenciamento:

- PostgreSQL: use, copy, modify, and distribute.

### Backend - API Rest

#### Flask Restful API

Construída com o framework Flask que é escrito na linguagem Python. Implementa os padrões REST e totalmente desacoplada dos demais componentes, o que permite fácil escalabilidade por containers Docker e manutenção.

- A grande vantagem deste tipo de integração, por ser restful, é a possibilidade dos tribunais regionais integrar com o seus geradores de json (DataJud) ou até mesmo utilizando integração com as bases dos sistemas transacionais.

Para servir as requisições em modo concorrente foi utilizado o WSGI Gunicorn que aumenta a escabilidade e o tratamento de requisições paralelas do flask.

##### Licenciamento:

- Flask: BSD License
- Gunicorn: The MIT License

#### Task Queue

- Celery: framework Python para gestão e execução de tarefas assíncronas. Utilizado para atualização e cargas de dados. Especificamente os endpoints para: carregar e validar todos os processos de um tribunal especifico; carregar e validar um único processo. A notificação dos usuários para os processos inconsistentes também será executada como uma tarefa assincrona pelo worker celery.
- Redis: estrutura de dados em memória utilizado como message broker entre a API e as tarefas assíncronas.

A solução utilizada uma estrutura de filas assincronas, justamente para prever futuras evoluções e altas cargas de dados.
Com a existência de um gerenciador de filas, bem como containers de workers isolados, a solução é possível de ser escalada horizontalmente.

##### Licenciamento:

- Celery: BSD License
- Redis: BSD License
  Frontend

##### Instruções para a execução do docker-compose

1. Criar um arquivo .env na pasta docker com os propriedades abaixo:

```
FLASK_ENV=dev
APP_PORT=5002
WORKERS=4
THREADS=2
WORKER_CLASS=gthread
DATABASE_URL=postgres://sanjus_app:XXXX@postgres:5432/sanjus
GUNICORN_CMD_ARGS=--bind '0.0.0.0:5002' --workers 8 --worker-class gthread --threads 2 --config python:config_gunicorn
DEBUG=True
prometheus_multiproc_dir=/tmp
METRICS_PORT=5003
TZ=America/Sao_Paulo
HOST_ELASTIC=time16-datajud.ddns.net
PORT_ELASTIC=9200
USER_ELASTIC=elastic
PASS_ELASTIC=XXXXX
CELERY_RESULT_BACKEND=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1
```

2. Automaticamente o container (sanjus_init) irá executar as migrations do banco de dados, abaixo detalhamos alguns comandos que podem ser utilizados para a geração automatizada de migrations.

Caso seja alterada alguma entidade do módulo src.entidades é necessário executar o alembic para que uma nova migration seja gerada para isso, deve-se acessar a pasta do projeto e executar o comando: `python manage.py db migrate`.
Após a execução do `migrate` será criado um novo arquivo .py dentro de migrations/versions. É recomendável a validação e atualização do arquivo antes de efetivar a migration. Para efetivar a migration o seguinte comando pode ser utilizado `python manage.py db upgrade`
Também é possível realizar downgrade e outros tipos de atualização conforme detalhamento [Documentação Alembic](https://alembic.sqlalchemy.org/en/latest/)

### Frontend

O Frontend está versionado no repositório git ![time16-frontend](https://github.com/jhcruvinel/time16)
Considerando que os fluxos dos processos são complexos, e extensos. A solução foi feita pensando no uso para desktop.
Justamente pela possível dificuldade em visualizar fluxos em dispositivos com telas reduzidas.

Desta forma a aplicação foi construída utilizando o framework Angular. Para melhorar a experiência do usuário foram utilizados os componentes da biblioteca Angular Material.

##### Licenciamento:

    ◦ Angular: The MIT License
    ◦ Angular Material: The MIT License


### Ambiente de execução

Para a disponibilização da aplicação utilizamos servidores (Droplets) da ![Digital Ocean](www.digitalocean.com). Como todos os componentes da solução estão em containers, o gerenciamento, bem como o monitoramento é feito de forma automatizada e ágil.
Todo o ambiente está rodando em uma VM com 4GB, e 2 processadores. 
Durante os testes e nos monitoramentos que realizamos o máximo de load que máquina chegou foi em 0,5.
![Load](doc/load-cpu.png)

Já o uso de memória RAM se mantém constante em 70%
![Memória](doc/memoria.png)


Acesso para a aplicação: ![Sanjus](http://time16-sanjus.ddns.net/)
