from os import getenv
from flask import Flask
from flask_restful import Api
from config import config, DataSources
from .apis import configure_api
from flask_sqlalchemy import SQLAlchemy
from .persistencia.database import configure_database


dataSource = 'datasource'


api = Api()


def create_app(versao):
    application = Flask(__name__)
    get_configuracao().APP_VERSION = versao
    application.config.from_object(get_configuracao())
    configure_database(application)
    configure_api(application, api, get_configuracao())
    api.init_app(application)
    return application


def get_configuracao():
    return config[(getenv('FLASK_ENV') or 'default')]


def get_datasource():
    return config[dataSource]
