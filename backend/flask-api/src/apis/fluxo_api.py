from flask import request, Response
from flask_restful import Resource
from ..servicos import fluxo_servico
from ..utils import helper
import json


class FluxoRIAPI(Resource):

    def get(self):
        try:
            retorno = [helper.serializar(fluxo)
                       for fluxo in fluxo_servico.listar_fluxo('S')]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


class FluxoAPI(Resource):

    def get(self):
        try:
            retorno = [helper.serializar(fluxo)
                       for fluxo in fluxo_servico.listar_fluxo('N')]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')



def configure_api(api):
    api.add_resource(
        FluxoRIAPI, '/fluxo/ri')
    api.add_resource(
        FluxoAPI, '/fluxo/principal')

