from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
from .health_check import configure_health_check
from .fluxo_processos import configure_api as fluxo_processo_api
from .evento_api import configure_api as evento_api
from .situacao_api import configure_api as situacao_api
from .prometheus_exporter import configure_prometheus


def configure_api(application, api, configuracao):
    configure_health_check(application, configuracao)
    metrics = GunicornPrometheusMetrics(app=application)
    configure_prometheus(application, metrics,  configuracao)
    fluxo_processo_api(api)
    evento_api(api)
    situacao_api(api)
