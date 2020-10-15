from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
from .health_check import configure_health_check
from .fluxo_processos import configure_api as fluxo_processo_api
from .prometheus_exporter import configure_prometheus


def configure_api(application, api, configuracao):
    configure_health_check(application, configuracao)
    metrics = GunicornPrometheusMetrics(app=application)
    configure_prometheus(application, metrics,  configuracao)
    fluxo_processo_api(api)
