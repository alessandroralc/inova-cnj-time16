from flask import request, Response
from flask_restful import Resource,reqparse, abort
from ..servicos import complemento_servico
from ..utils import helper
import json
import traceback


class ComplementoAPI(Resource):

    def get(self):
        try:
            retorno = [helper.serializar(evento)
                       for evento in complemento_servico.listar_complementos()]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')

    def post(self):
        try:
            body = json.loads(request.get_data().decode('UTF-8'))
            if body:
                id_complemento = complemento_servico.incluir_complemento(body)
                return Response(json.dumps({"id_complemento": id_complemento}), status=201)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')

    def delete(self):
        try:
            body = json.loads(request.get_data().decode('UTF-8'))
            if body:
                complemento_servico.remover_complemento(body.get('id_complemento'))
                return Response('Registro excluído com sucesso', status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


    def put(self):
        parser.add_argument('id_complemento', required=True, location='json', type=int,
            help="XXXXXXXXXXXXXx")
        parser.add_argument('cd_tpu_complemento', required=True, location='json', type=str,
            help="XXXXXXXXXXXXX.")
        parser.add_argument('vl_complemento', required=True, location='json', type=str,
            help="XXXXXXXXXXXXXXXXX")
        parser.add_argument('id_movimento', required=True, location='json', type=int,
            help="XXXXXXXXXXXXXXXXX")

        args = parser.parse_args()

        return complemento_servico.atualizar_complemento(args)






def configure_api(api):
    api.add_resource(
        ComplementoAPI, '/api/v1.0/complemento')
