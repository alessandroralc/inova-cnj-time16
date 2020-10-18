from flask import request, Response
from flask_restful import Resource
from ..servicos import situacao_servico
from ..utils import helper
import json


class SituacaoAPI(Resource):

    def get(self):
        try:
            retorno = [helper.serializar(situacao)
                       for situacao in situacao_servico.listar_situacoes()]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


def configure_api(api):
    api.add_resource(
        SituacaoAPI, '/situacoes')
