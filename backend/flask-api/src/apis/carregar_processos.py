from flask import request, Response
from flask_restful import Resource
import json
import traceback
from ..servicos.carga_processos import carregar_dados_processos


class CarregarProcessos(Resource):

    def post(self):
        try:
            body = json.loads(request.get_data().decode('UTF-8'))
            retorno = {
                "mensagem": f"A carga foi iniciada com sucesso em segundo plano para {body['cod_tribunal']} {body['cod_instancia']}"
            }
            carregar_dados_processos(body['cod_tribunal'], body['cod_instancia'])
            return Response(json.dumps(retorno), status=201)
        except:
            traceback.print_exc()
            return Response('Error', status=500, mimetype='application/json')


def configure_api(api):
    api.add_resource(
        CarregarProcessos, '/carregar/processos')
