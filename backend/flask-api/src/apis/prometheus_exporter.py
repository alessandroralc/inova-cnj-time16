from flask import request


def configure_prometheus(app, metrics, configuracao):
    metrics.info('app_info',
                 'Informações da aplicaçao', version=configuracao.APP_VERSION)
    metrics.register_default(
        metrics.counter(
            'outside_context',
            'Contexto da aplicação',
            labels={'endpoint': lambda: request.endpoint}
        ),
        app=app)

    metrics.register_default(
        metrics.counter(
            'by_path_counter', 'Contador de requisições',
            labels={'path': lambda: request.path}
        ),
        app=app
    )
