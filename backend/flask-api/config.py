import os
from os import getenv
from os.path import dirname, isfile, join
from dotenv import load_dotenv
from sqlalchemy.engine.url import URL

_ENV_FILE = join(dirname(__file__), 'config.env')


if isfile(_ENV_FILE):
    load_dotenv(dotenv_path=_ENV_FILE)


class Config:
    APP_VERSION = ''
    SECRET_KEY = getenv('SECRET_KEY')
    APP_PORT = int(getenv('APP_PORT'))
    DEBUG = (getenv('DEBUG') or 'True')
    GIT_REPO = 'https://github.com/lucasbibianot/inova-cnj-time16'
    MAINTAINER = 'Desafio 2 Time 16'
    METRICS_PORT = int(getenv('METRICS_PORT'))
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_BINDS = {
        'sanjus': URL(**{
            'drivername': 'postgres+psycopg2',
            'host': getenv('POSTGRES_HOST'),
            'port': getenv('POSTGRES_PORT'),
            'username': getenv('POSTGRES_USERNAME'),
            'password': getenv('POSTGRES_PASS') ,
            'database': getenv('POSTGRES_DATABASE')
        })
    }


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True


class ProductionConfig(Config):
    FLASK_ENV = 'producao'
    DEBUG = False


class DataSources():
    def __init__(self, db):
        self.db = db


config = {
    'dev': DevelopmentConfig,
    'default': DevelopmentConfig,
    'prod': ProductionConfig,
    'hom': DevelopmentConfig,
    'db': DataSources
}
