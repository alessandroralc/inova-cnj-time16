import re
from ..entidades.modelo_fluxo import GrupoSituacao
from ..persistencia.database import db
from flask_restful import abort
from flask import  Response
import json

def incluir_grupo(parametros):
    grupo = GrupoSituacao(**parametros)
    grupo.id_grupo = None
    db.session.add(grupo)
    db.session.commit()
    return grupo.id_grupo


def remover_grupo(id_grupo):
    db.session.query(GrupoSituacao).filter(
        GrupoSituacao.id_grupo == id_grupo).delete()
    db.session.commit()


def listar_grupos():
    return GrupoSituacao.query.all()


def listar_grupos_id(id_grupo):
    return db.session.query(GrupoSituacao).filter(GrupoSituacao.id_grupo == id_grupo).all()


def listar_grupos_filtro(cd_tribunal, cd_grau):
    return db.session.query(GrupoSituacao).filter(GrupoSituacao.sg_tribunal == cd_tribunal and GrupoSituacao.sg_grau == cd_grau).all()


def atualizar_grupo(data_json):
    
    try:
        db_obj = GrupoSituacao.query.filter(GrupoSituacao.id_grupo == int(data_json['id_grupo'])).one()
    
    except (exc.NoResultFound, exc.MultipleResultsFound) as error:
        return abort(404, message="ERRO: {}".format(error))    
    
    else:
        
        for key, value in data_json.items():
            setattr(db_obj, key, value)
       

        try:        
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return abort(404, message="ERRO: {}".format(error))
        
                
        
        return Response(json.dumps({'message':'Situacao com id {} atualizada.'.format(vars(db_obj))}), status=200)
