from flask import request, Response
from flask_restful import Resource
from ..servicos import fluxo_servico
from ..utils import helper
import json
import traceback


class TribunalAPI(Resource):

    def get(self):
        try:
            retorno = fluxo_servico.retornar_tribunais_com_fluxo()
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


class TribunalGrauAPI(Resource):

    def get(self, cod_tribunal):
        try:
            retorno = fluxo_servico.retornar_graus_com_fluxo(cod_tribunal)
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


def configure_api(api):
    api.add_resource(
        TribunalAPI, '/api/v1.0/tribunal')
    api.add_resource(TribunalGrauAPI, '/api/v1.0/grau/<string:cod_tribunal>')