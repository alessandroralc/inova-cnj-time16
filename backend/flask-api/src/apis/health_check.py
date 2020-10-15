from healthcheck import HealthCheck, EnvironmentDump
import datetime


def configure_health_check(app, config):
    health = HealthCheck()
    configuracao = config
    envdump = EnvironmentDump()
    app.add_url_rule('/healthcheck', 'healthcheck',
                     view_func=lambda: health.run())
    app.add_url_rule('/environment', 'environment',
                     view_func=lambda: envdump.run())
