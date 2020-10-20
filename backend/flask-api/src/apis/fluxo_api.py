from flask import request, Response
from flask_restful import Resource
from ..servicos import fluxo_servico
from ..utils import helper
import json
import traceback


class FluxoAPI(Resource):

    def get(self):
        try:
            retorno = [helper.serializar(fluxo)
                       for fluxo in fluxo_servico.listar_fluxo('N')]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')

    def post(self):
        try:
            body = json.loads(request.get_data().decode('UTF-8'))
            if body:
                id_fluxo = fluxo_servico.incluir_fluxo(body)
                return Response(json.dumps({"id_fluxo": id_fluxo}), status=201)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')

    def delete(self):
        try:
            body = json.loads(request.get_data().decode('UTF-8'))
            if body:
                fluxo_servico.remover_fluxo(body.get('id_fluxo'))
                return Response('Registro excluído com sucesso', status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')

    def put(self):
        parser.add_argument('id_fluxo_movimento', required=True, location='json', type=int,
            help="XXXXXXXXXXXXXx")
        parser.add_argument('id_situacao_origem', required=True, location='json', type=int,
            help="XXXXXXXXXXXXX.")
        parser.add_argument('id_evento', required=True, location='json', type=int,
            help="XXXXXXXXXXXXXXXXX")
        parser.add_argument('id_situacao_destino', required=True, location='json', type=int,
            help="XXXXXXXXXXXXXXXX")
        parser.add_argument('ind_consistente', required=True, location='json',type=str,
            help="XXXXXXXXXXXXXXXX")
        parser.add_argument('ind_efetiva', required=True, location='json',type=str,
            help="XXXXXXXXXXXXXXXX")
        parser.add_argument('ind_fluxo_ri', required=True, location='json',type=str,
            help="XXXXXXXXXXXXXXXX")
        parser.add_argument('id_grupo', required=True, location='json', type=int,
            help="XXXXXXXXXXXXXXXX")
        parser.add_argument('sg_tribunal', required=True, location='json',type=str,
            help="XXXXXXXXXXXXXXXX")
        parser.add_argument('sg_grau', required=False, location='json',type=str,
            help="XXXXXXXXXXXXXXXX")
        
        args = parser.parse_args()
    
        return fluxo_servico.atualizar_fluxo(args)


class FluxoFiltroAPI(Resource):

    def get(self, cd_tribunal, cd_grau):
        try:
            retorno = [helper.serializar(fluxo)
                       for fluxo in fluxo_servico.listar_fluxo_filtro('N', cd_tribunal, cd_grau)]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


class FluxoIdAPI(Resource):

    def get(self, id_fluxo):
        try:
            retorno = [helper.serializar(fluxo)
                       for fluxo in fluxo_servico.listar_fluxo_id(id_fluxo)]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


class FluxoDirRede(Resource):

    def get(self, cd_tribunal, cd_grau, ind_consistente):
        try:
            retorno = fluxo_servico.gerar_transicoes_rede(cd_tribunal, cd_grau, ind_consistente)
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')



class FluxoDirArvore(Resource):

    def get(self, cd_tribunal, cd_grau, ind_consistente):
        try:
            retorno = fluxo_servico.gerar_transicoes_arvore(cd_tribunal, cd_grau, ind_consistente)
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


def configure_api(api):
    api.add_resource(
        FluxoAPI, '/api/v1.0/fluxo')
    api.add_resource(
        FluxoIdAPI, '/api/v1.0/fluxo/<int:id_fluxo>')
    api.add_resource(
        FluxoFiltroAPI, '/api/v1.0/fluxo/<string:cd_tribunal>/<string:cd_grau>')
    api.add_resource(
        FluxoDirRede, '/api/v1.0/fluxo/rede/<string:cd_tribunal>/<string:cd_grau>/<string:ind_consistente>')        
    api.add_resource(
        FluxoDirArvore, '/api/v1.0/fluxo/arvore/<string:cd_tribunal>/<string:cd_grau>/<string:ind_consistente>')   
