import re
from ..entidades.modelo_fluxo import Movimento
from ..persistencia.database import db
from sqlalchemy.orm import aliased,load_only,Load,exc
from flask_restful import abort
from flask import  Response
import json


def incluir_movimento(parametros):
    movimento = Movimento(**parametros)
    movimento.id_movimento = None
    db.session.add(movimento)
    db.session.commit()
    return movimento.id_movimento


def remover_movimento(id_movimento):
    db.session.query(Movimento).filter(
        Movimento.id_movimento == id_movimento).delete()
    db.session.commit()


def listar_movimentos():
    return Movimento.query.all()


def listar_movimentos_evento(id_evento):
    return db.session.query(Movimento).filter(Movimento.id_evento == id_evento).all()


def listar_movimentos_id(id_movimento):
    return db.session.query(Movimento).filter(Movimento.id_movimento == id_movimento).all()


def atualizar_movimento(data_json):
    
    try:
        obj_db = Movimento.query.filter(Movimento.id_movimento == int(data_json['id_movimento'])).one()
    
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
        
                
        
        return Response(json.dumps({'message':'Situacao com id {} atualizada.'.format(obj_db.id_movimento)}), status=200)
