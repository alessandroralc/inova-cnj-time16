from flask import request, Response
from flask_restful import Resource
from ..servicos import grupo_servico
from ..servicos import situacao_servico
from ..utils import helper
import json
import traceback


class GrupoAPI(Resource):

    def get(self):
        try:
            retorno = [helper.serializar(evento)
                       for evento in grupo_servico.listar_grupos()]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')

    def post(self):
        try:
            body = json.loads(request.get_data().decode('UTF-8'))
            if body:
                id_evento = grupo_servico.incluir_grupo(body)
                return Response(json.dumps({"id_grupo": id_evento}), status=201)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')

    def delete(self):
        try:
            body = json.loads(request.get_data().decode('UTF-8'))
            if body:
                grupo_servico.remover_grupo(body.get('id_grupo'))
                return Response('Registro excluído com sucesso', status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')

    def put(self):
        parser.add_argument('id_grupo', required=True, location='json', type=int,
            help="XXXXXXXXXXXXXx")
        parser.add_argument('ds_grupo', required=True, location='json', type=str,
            help="XXXXXXXXXXXXX.")
        parser.add_argument('cd_grupo', required=True, location='json', type=str,
            help="XXXXXXXXXXXXXXXXX")
        parser.add_argument('sg_tribunal', required=True, location='json', type=str,
            help="XXXXXXXXXXXXXXXX")
        parser.add_argument('sg_grau', required=True, location='json',type=str,
            help="XXXXXXXXXXXXXXXX")
             
        args = parser.parse_args()
        
        return grupo_servico.atualizar_grupo(args)



class GrupoIdAPI(Resource):

    def get(self, id_grupo):
        try:
            retorno = [helper.serializar(evento)
                       for evento in grupo_servico.listar_grupos_id(id_grupo)]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


class GrupoFiltroAPI(Resource):

    def get(self, cd_tribunal, cd_grau):
        try:
            retorno = [helper.serializar(evento)
                       for evento in grupo_servico.listar_grupos_filtro(cd_tribunal, cd_grau)]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


class GrupoSituacaoAPI(Resource):

    def get(self, cd_tribunal, cd_grau):
        try:
            retorno = [helper.serializar(evento)
                       for evento in situacao_servico.listar_situacoes_grupo(id_grupo)]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')



def configure_api(api):
    api.add_resource(
        GrupoAPI, '/api/v1.0/grupo')
    api.add_resource(
        GrupoIdAPI, '/api/v1.0/grupo/<int:id_grupo>')
    api.add_resource(
        GrupoSituacaoAPI, '/api/v1.0/grupo/<int:id_grupo>/situacao')        
    api.add_resource(
        GrupoFiltroAPI, '/api/v1.0/grupo/<string:cd_tribunal>/<string:cd_grau>')
