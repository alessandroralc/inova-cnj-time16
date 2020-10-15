from os import getenv
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
from src import get_configuracao


def when_ready(server):
    GunicornPrometheusMetrics.start_http_server_when_ready(
        int(get_configuracao().METRICS_PORT))


def child_exit(server, worker):
    GunicornPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)
