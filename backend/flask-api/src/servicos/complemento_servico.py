import re
from ..entidades.modelo_fluxo import Complemento
from ..persistencia.database import db
from sqlalchemy.orm import aliased,load_only,Load,exc
from flask_restful import abort
from flask import  Response
import json


def incluir_complemento(parametros):
    complemento = Complemento(**parametros)
    complemento.id_movimento = None
    db.session.add(complemento)
    db.session.commit()
    return complemento.id_movimento


def remover_complemento(id_complemento):
    db.session.query(Complemento).filter(
        Complemento.id_movimento == id_complemento).delete()
    db.session.commit()


def listar_complementos():
    return Complemento.query.all()


def listar_complementos_id(id_movimento):
    return db.session.query(Complemento).filter(Complemento.id_complemento == id_complemento).all()


def atualizar_complemento(data_json):
    
    try:
        obj_db = Complemento.query.filter(Complemento.id_complemento == int(data_json['id_complemento'])).one()
    
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
        
                
        
        return Response(json.dumps({'message':'Situacao com id {} atualizada.'.format(obj_db.id_complemento)}), status=200)
