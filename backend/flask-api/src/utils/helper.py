import decimal
import json
import datetime
import math
import locale
from collections import Counter

def serializar(obj):
    return {k: v for (k, v) in vars(obj).items()
            if not str(k).startswith('_')}

def serializar_lista(lista_de_tupla):
    #if len(lista_de_tupla) == 0:
    #    return {}
    lista_de_dicionario = [serializar(obj) for obj in lista_de_tupla]
    
    #Deal with objects from the same table like Situacao.ds_situacao origem e destino
    out_dict = {}
    repeated_key_counter = Counter()    
    for d in lista_de_dicionario:
        for k,v in d.items():
            if out_dict.get(k) is None:
                out_dict[k] = v
            else:
                repeated_key_counter[k]+=1
                k+='_'+str(repeated_key_counter[k]+1)
                out_dict[k] = v    
                  

    return out_dict
        



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
