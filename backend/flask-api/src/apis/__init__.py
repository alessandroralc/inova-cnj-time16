from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
from .health_check import configure_health_check
from .fluxo_processos import configure_api as fluxo_processo_api
from .evento_api import configure_api as evento_api
from .situacao_api import configure_api as situacao_api
from .fluxo_api import configure_api as fluxo_api
from .prometheus_exporter import configure_prometheus
from .carregar_processos import configure_api as carregar_processos_api
from .tribunal_api import configure_api as tribunal_api
from .grupo_api import configure_api as grupo_api

from .orair_api import configure_api as orair_api

from .movimento_api import configure_api as movimento_api


def configure_api(application, api, configuracao):
    configure_health_check(application, configuracao)
    metrics = GunicornPrometheusMetrics(app=application)
    configure_prometheus(application, metrics,  configuracao)
    fluxo_processo_api(api)
    evento_api(api)
    situacao_api(api)
    fluxo_api(api)
    carregar_processos_api(api)
    tribunal_api(api)
    grupo_api(api)

    orair_api(api)
    

    movimento_api(api)

