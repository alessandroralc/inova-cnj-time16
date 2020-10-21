from flask import request, Response
from flask_restful import Resource,reqparse, abort
from ..servicos import orair_servico
from ..utils import helper
import json
import traceback


class TransacaoValidaAPI(Resource):

    def get(self):
        try:
            retorno = [helper.serializar(evento)
                       for evento in orair_servico.listar_transicoes_valida()]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')

    def post(self):
        try:
            body = json.loads(request.get_data().decode('UTF-8'))
            if body:
                id_movimento = orair_servico.incluir_transicao_valida(body)
                return Response(json.dumps({"id_movimento": id_movimento}), status=201)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')

    def delete(self):
        try:
            body = json.loads(request.get_data().decode('UTF-8'))
            if body:
                orair_servico.remover_transicao_valida(body.get('id_movimento'))
                return Response('Registro excluído com sucesso', status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


    def put(self):
        
        parser.add_argument('id_transicao', required=True, location='json', type=int,
            help="XXXXXXXXXXXXXx")
        parser.add_argument('id_situacao_origem', required=True, location='json', type=int,
            help="XXXXXXXXXXXXXx")
        parser.add_argument('id_evento', required=True, location='json', type=int,
            help="XXXXXXXXXXXXXx")
        parser.add_argument('id_situacao_destino', required=True, location='json', type=int,
            help="XXXXXXXXXXXXXx")
        parser.add_argument('ind_consistente', required=True, location='json', type=str,
            help="XXXXXXXXXXXXXx")
        parser.add_argument('ind_efetiva', required=True, location='json', type=str,
            help="XXXXXXXXXXXXXx")
        parser.add_argument('sg_tribunal', required=True, location='json', type=str,
            help="XXXXXXXXXXXXXx")
        parser.add_argument('sg_grau', required=True, location='json', type=str,
            help="XXXXXXXXXXXXXx")

        args = parser.parse_args()

        return orair_servico.atualizar_transicao_valida(args)



class TransacaoGrupoValidaAPI(Resource):

    def get(self):
        try:
            retorno = [helper.serializar(evento)
                       for evento in orair_servico.listar_transicoes_grupo_valida()]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')

    def post(self):
        try:
            body = json.loads(request.get_data().decode('UTF-8'))
            if body:
                id_movimento = orair_servico.incluir_transicao_grupo_valida(body)
                return Response(json.dumps({"id_movimento": id_movimento}), status=201)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')

    def delete(self):
        try:
            body = json.loads(request.get_data().decode('UTF-8'))
            if body:
                orair_servico.remover_transicao_grupo_valida(body.get('id_movimento'))
                return Response('Registro excluído com sucesso', status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


    def put(self):
        
        parser.add_argument('id_transicao_grp', required=True, location='json', type=int,
            help="XXXXXXXXXXXXXx")
        parser.add_argument('id_grupo', required=True, location='json', type=int,
            help="XXXXXXXXXXXXXx")
        parser.add_argument('id_evento', required=True, location='json', type=int,
            help="XXXXXXXXXXXXXx")
        parser.add_argument('id_situacao_destino', required=True, location='json', type=int,
            help="XXXXXXXXXXXXXx")
        parser.add_argument('ind_consistente', required=True, location='json', type=str,
            help="XXXXXXXXXXXXXx")
        parser.add_argument('ind_efetiva', required=True, location='json', type=str,
            help="XXXXXXXXXXXXXx")
        parser.add_argument('sg_tribunal', required=True, location='json', type=str,
            help="XXXXXXXXXXXXXx")
        parser.add_argument('sg_grau', required=True, location='json', type=str,
            help="XXXXXXXXXXXXXx")

        args = parser.parse_args()

        return orair_servico.atualizar_transicao_grupo_valida(args)




def configure_api(api):
    api.add_resource(
        TransacaoValidaAPI, '/api/v1.0/transicaovalida')
    api.add_resource(
        TransacaoGrupoValidaAPI, '/api/v1.0/transicaogrupovalida')
