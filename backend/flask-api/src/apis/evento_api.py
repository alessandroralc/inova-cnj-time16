from flask import request, Response
from flask_restful import Resource
from ..servicos import eventos_servico
from ..utils import helper
import json


class EventoAPI(Resource):

    def get(self):
        try:
            retorno = [helper.serializar(evento)
                       for evento in eventos_servico.listar_eventos()]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


def configure_api(api):
    api.add_resource(
        EventoAPI, '/eventos')
