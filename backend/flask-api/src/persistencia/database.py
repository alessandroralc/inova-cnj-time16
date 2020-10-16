from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def configure_database(app):
    db.init_app(app)
