from json import encoder
from flask import request, Response
from flask_restful import Resource, reqparse, abort
from ..servicos import situacao_servico
from ..utils import helper
from ..persistencia.database import db
import json
import traceback


parser = reqparse.RequestParser()


class SituacaoAPI(Resource):

    def get(self):
        try:
            retorno = [helper.serializar(situacao)
                       for situacao in situacao_servico.listar_situacoes()]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')

    def post(self):
        try:
            body = json.loads(request.get_data().decode('UTF-8'))
            print(body)
            if body:
                id_situacao = situacao_servico.incluir_situacao(body)
                return Response(json.dumps({"id_situacao": id_situacao}), status=201)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')

    def put(self):
        parser.add_argument('id_situacao', required=True, location='json', type=int,
                            help="XXXXXXXXXXXXXx")
        parser.add_argument('ds_situacao', required=True, location='json', type=str,
                            help="XXXXXXXXXXXXX.")
        parser.add_argument('cd_situacao', required=True, location='json', type=str,
                            help="XXXXXXXXXXXXXXXXX")
        parser.add_argument('ind_principal', required=True, location='json', type=str,
                            help="XXXXXXXXXXXXXXXX")
        parser.add_argument('ind_ri', required=True, location='json', type=str,
                            help="XXXXXXXXXXXXXXXX")
        parser.add_argument('sg_tribunal', required=True, location='json', type=str,
                            help="XXXXXXXXXXXXXXXX")
        parser.add_argument('sg_grau', required=True, location='json', type=str,
                            help="XXXXXXXXXXXXXXXX")
        parser.add_argument('fl_inicio', required=True, location='json', type=str,
                            help="XXXXXXXXXXXXXXXX")
        parser.add_argument('fl_fim', required=True, location='json', type=str,
                            help="XXXXXXXXXXXXXXXX")
        parser.add_argument('id_grupo', required=False, location='json', type=int,
                            help="XXXXXXXXXXXXXXXX")

        args = parser.parse_args()

        return situacao_servico.atualizar_situacao(args)


class SituacaoFiltroAPI(Resource):

    def get(self, cod_tribunal, cod_instancia):
        try:
            retorno = [helper.serializar(situacao)
                       for situacao in situacao_servico.listar_situacoes_filtro(cod_tribunal, cod_instancia)]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


class SituacaoIdAPI(Resource):

    def get(self, id_situacao):
        try:
            retorno = [helper.serializar(situacao)
                       for situacao in situacao_servico.listar_situacoes_id(id_situacao)]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')

    def delete(self, id_situacao):
        try:
            situacao_servico.remover_situacao(id_situacao)
            return Response('Registro excluído com sucesso', status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


class SituacaoProcesso(Resource):

    def get(self, str_consistente):
        try:
            retorno = [helper.serializar_lista(situacao)
                       for situacao in situacao_servico.listar_processos_consistencia(str_consistente)]
            return Response(json.dumps(retorno, cls=helper.JSONEnconder), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


class FluxoOfProcesso(Resource):

    def get(self, id_processo):
        try:
            retorno = [helper.serializar_lista(situacao)
                       for situacao in situacao_servico.listar_fluxo_processo(id_processo)]

            return Response(json.dumps(retorno, cls=helper.JSONEnconder), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


def configure_api(api):
    api.add_resource(
        SituacaoAPI, '/api/v1.0/situacao')
    api.add_resource(
        SituacaoIdAPI, '/api/v1.0/situacao/<int:id_situacao>')
    api.add_resource(
        SituacaoFiltroAPI, '/api/v1.0/situacao/<string:cod_tribunal>/<string:cod_instancia>')
    api.add_resource(
        SituacaoProcesso, '/api/v1.0/situacao/<string:str_consistente>')
    api.add_resource(
        FluxoOfProcesso, '/api/v1.0/situacao/processo/<string:id_processo>')
