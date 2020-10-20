from flask import request, Response
from flask_restful import Resource,reqparse, abort
from ..servicos import movimento_servico
from ..utils import helper
import json
import traceback


class MovimentoAPI(Resource):

    def get(self):
        try:
            retorno = [helper.serializar(evento)
                       for evento in movimento_servico.listar_movimentos()]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')

    def post(self):
        try:
            body = json.loads(request.get_data().decode('UTF-8'))
            if body:
                id_movimento = movimento_servico.incluir_movimento(body)
                return Response(json.dumps({"id_evento": id_movimento}), status=201)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')

    def delete(self):
        try:
            body = json.loads(request.get_data().decode('UTF-8'))
            if body:
                movimento_servico.remover_movimento(body.get('id_movimento'))
                return Response('Registro excluído com sucesso', status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


    def put(self):
        parser.add_argument('id_movimento', required=True, location='json', type=int,
            help="XXXXXXXXXXXXXx")
        parser.add_argument('cd_tpu_movimento', required=True, location='json', type=str,
            help="XXXXXXXXXXXXX.")
        parser.add_argument('id_evento', required=True, location='json', type=int,
            help="XXXXXXXXXXXXXXXXX")

        args = parser.parse_args()

        return movimento_servico.atualizar_movimento(args)






def configure_api(api):
    api.add_resource(
        MovimentoAPI, '/api/v1.0/movimento')
