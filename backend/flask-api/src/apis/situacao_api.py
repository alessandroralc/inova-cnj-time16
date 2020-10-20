from json import encoder
from flask import request, Response
from flask_restful import Resource
from ..servicos import situacao_servico
from ..utils import helper
import json
import traceback


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
            retorno = situacao_servico.listar_processos_consistencia(
                str_consistente)
            return Response(json.dumps(retorno, cls=helper.JSONEnconder), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


class FluxoOfProcesso(Resource):

    def get(self, id_processo):
        try:
            retorno = situacao_servico.listar_fluxo_processo(id_processo)
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
