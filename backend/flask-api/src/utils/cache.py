import requests_cache
import datetime


def session_cache_request(duracao=30):
    expire_after = datetime.timedelta(minutes=duracao)
    return requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)


def cache_request(duracao=30):
    expire_after = datetime.timedelta(minutes=duracao)
    return requests_cache.enabled(cache_name='cache', backend='sqlite', expire_after=expire_after)
