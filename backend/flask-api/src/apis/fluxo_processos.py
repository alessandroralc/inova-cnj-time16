from flask import request, Response
from flask_restful import Resource
import json


class FluxoProcesso(Resource):

    def get(self, cod_fluxo):
        try:
            retorno = {
                "mensagem": "Sucesso",
                "parametro" : cod_fluxo
            }
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


def configure_api(api):
    api.add_resource(
        FluxoProcesso, '/fluxoprocesso/transicoes/<string:cod_fluxo>')
