from celery import Celery

celery = Celery()

def make_celery(app):
    celery_= Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery_.conf.update(app.config)

    class ContextTask(celery_.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_.Task = ContextTask
    return celery_


def set_celery(celery_):
    celery = celery_