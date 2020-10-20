import re
from ..entidades.modelo_fluxo import Evento
from ..persistencia.database import db
from sqlalchemy.orm import aliased,load_only,Load,exc
from flask_restful import abort
from flask import  Response
import json


def incluir_evento(parametros):
    evento = Evento(**parametros)
    evento.id_evento = None
    db.session.add(evento)
    db.session.commit()
    return evento.id_evento


def remover_evento(id_evento):
    db.session.query(Evento).filter(
        Evento.id_evento == id_evento).delete()
    db.session.commit()


def listar_eventos():
    return Evento.query.all()

def listar_eventos_id(id_evento):
    return db.session.query(Evento).filter(Evento.id_evento == id_evento).all()


def atualizar_evento(data_json):
    
    try:
        obj_db = Evento.query.filter(Evento.id_evento == int(data_json['id_evento'])).one()
    
    except (exc.NoResultFound, exc.MultipleResultsFound) as error:
        return abort(404, message="ERRO: {}".format(error))    
    
    else:
        
        for key, value in data_json.items():
            setattr(obj_db, key, value)
       

        try:        
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return abort(404, message="ERRO: {}".format(error))
        
                
        
        return Response(json.dumps({'message':'Situacao com id {} atualizada.'.format(obj_db.id_evento)}), status=200)
