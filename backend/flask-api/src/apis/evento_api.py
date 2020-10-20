from flask import request, Response
from flask_restful import Resource,reqparse, abort
from ..servicos import evento_servico
from ..servicos import movimento_servico
from ..utils import helper
import json
import traceback


class EventoAPI(Resource):

    def get(self):
        try:
            retorno = [helper.serializar(evento)
                       for evento in evento_servico.listar_eventos()]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')

    def post(self):
        try:
            body = json.loads(request.get_data().decode('UTF-8'))
            if body:
                id_evento = evento_servico.incluir_evento(body)
                return Response(json.dumps({"id_evento": id_evento}), status=201)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')

    def put(self):
        body = json.loads(request.get_data().decode('UTF-8'))        
        return evento_servico.atualizar_evento(body)
      

class EventoIdAPI(Resource):

    def get(self, id_evento):
        try:
            retorno = [helper.serializar(evento)
                       for evento in evento_servico.listar_eventos_id(id_evento)]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')

    def delete(self, id_evento):
        try:
            evento_servico.remover_evento(id_evento)
            return Response('Registro excluído com sucesso', status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


class EventoMovimentoAPI(Resource):

    def get(self, id_evento):
        try:
            retorno = [helper.serializar(evento)
                       for evento in movimento_servico.listar_movimentos_evento(id_evento)]
            return Response(json.dumps(retorno), status=200)
        except Exception as e:
            traceback.print_exc()
            return Response('error: \'{0}\''.format(''.join(e.args)), status=500, mimetype='application/json')


def configure_api(api):
    api.add_resource(
        EventoAPI, '/api/v1.0/evento')
    api.add_resource(
        EventoIdAPI, '/api/v1.0/evento/<int:id_evento>')
    api.add_resource(
        EventoMovimentoAPI, '/api/v1.0/evento/<int:id_evento>/movimento')
