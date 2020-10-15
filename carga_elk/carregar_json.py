import requests
import json
import os
from elasticsearch import Elasticsearch
from requests.auth import HTTPBasicAuth

directory = '/mnt/DADOS/TRT/Inova CNJ/justica_trabalho/processos-trt{0}/'


res = requests.get('http://localhost:9200',
                   auth=HTTPBasicAuth('elastic', 'gTFMkGkGMKG2WGv1EoZe'))
print(res.content)
es = Elasticsearch([{'host': 'localhost', 'port': '9200'}],
                   http_auth=('elastic', 'gTFMkGkGMKG2WGv1EoZe'))


def carregar_arquivos(cod_trt):
    for filename in os.listdir(directory.format(cod_trt)):
        if filename.endswith(".json"):
            print(''.join([directory.format(cod_trt), filename]))
            with open(''.join([directory.format(cod_trt), filename])) as f:
                docket_content = f.read()
                # Send the data into es
                processos = json.loads(docket_content)
                for proc in processos:
                    indice = '_'.join([proc['siglaTribunal'], proc['grau'], str(
                        proc['dadosBasicos']['numero']), str(proc['dadosBasicos']['classeProcessual'])])
                    try:
                        es.index(index='datajud_jt', ignore=400,
                                 doc_type='docket', id=indice, body=proc)
                    except:
                        print(f'Erro ao incluir {indice}')
            os.remove(''.join([directory.format(cod_trt), filename]))


def principal():
    for i in range(1, 25):
        carregar_arquivos(i)


if __name__ == "__main__":
    principal()
