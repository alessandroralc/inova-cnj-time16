import decimal
import json
import datetime
import math
import locale


def serializar(obj):
    return {k: v for (k, v) in vars(obj).items()
            if not str(k).startswith('_')}


class JSONEnconder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()
        if isinstance(o, complex):
            return float(o.real)
        return super(JSONEnconder, self).default(o)


def converte_decimal(texto):
    return decimal.Decimal(str(texto).replace('.', '').replace(',', '.')) if texto else 0


def formata_data_iso(data):
    if(not data):
        return None
    data_obj = datetime.datetime.strptime(
        data, '%d/%m/%Y') if len(data) == 10 else datetime.datetime.strptime(data, '%d/%m/%y')
    return data_obj.strftime('%Y-%m-%d')


def formata_data_iso_from_texto(data_texto):
    if(not data_texto):
        return None
    locale.setlocale(locale.LC_ALL, 'pt_BR')
    return datetime.datetime.strptime(data_texto, '%b.-%Y').strftime('%Y-%m-%d')


def modulo_valor(valor):
    return math.fabs(valor)
