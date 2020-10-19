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
    APP_PORT = int(getenv('APP_PORT')) if getenv('APP_PORT') else 9999
    DEBUG = (getenv('DEBUG') or 'True')
    GIT_REPO = 'https://github.com/lucasbibianot/inova-cnj-time16'
    MAINTAINER = 'Desafio 2 Time 16'
    METRICS_PORT = int(getenv('METRICS_PORT')) if getenv('METRICS_PORT') else 9991
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    CSRF_ENABLED = True
    CORS_HEADERS = 'Content-Type'


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
