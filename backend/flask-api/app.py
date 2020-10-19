from celery import Celery
from flask_cors import CORS
from src import create_app
from src.celery.celery_init import make_celery, set_celery

application = create_app('0.1.5')
celery = make_celery(application)
set_celery(celery)
cors = CORS(application, resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
    ip = '0.0.0.0'
    port = application.config['APP_PORT']
    debug = application.config['DEBUG']

    application.run(
        host=ip, debug=debug, port=port, use_reloader=debug
    )
