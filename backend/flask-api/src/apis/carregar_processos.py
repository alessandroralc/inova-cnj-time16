from flask import request, Response
from flask_restful import Resource
import json
import traceback
from ..servicos.carga_processos import carregar_dados_processos, carregar_dados_processo


class CarregarProcessos(Resource):

    def post(self):
        try:
            body = json.loads(request.get_data().decode('UTF-8'))
            retorno = {
                "mensagem": f"A carga foi iniciada com sucesso em segundo plano para {body['cod_tribunal']} {body['cod_instancia']}"
            }
            result = carregar_dados_processos.delay(
                body['cod_tribunal'], body['cod_instancia'], body['realizar_limpeza'])
            return Response(json.dumps(retorno), status=201)
        except:
            traceback.print_exc()
            return Response('Error', status=500, mimetype='application/json')


class CarregarUnicoProcesso(Resource):

    def post(self):
        try:
            body = json.loads(request.get_data().decode('UTF-8'))
            retorno = {
                "mensagem": f"A carga foi iniciada com sucesso em segundo plano para {body['cod_tribunal']} {body['cod_instancia']}"
            }
            result = carregar_dados_processo.delay(
                body['cod_tribunal'], body['cod_instancia'], body['cd_processo'])
            return Response(json.dumps(retorno), status=201)
        except:
            traceback.print_exc()
            return Response('Error', status=500, mimetype='application/json')


def configure_api(api):
    api.add_resource(
        CarregarProcessos, '/api/v1.0/processo/carga/completa')
    api.add_resource(
        CarregarUnicoProcesso, '/api/v1.0/processo/carga')
