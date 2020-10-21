import re
from ..entidades.modelo_fluxo import TransacaoValida,TransicaoGrupoValida
from ..persistencia.database import db
from sqlalchemy.orm import aliased,load_only,Load,exc
from flask_restful import abort
from flask import  Response
import json


def listar_transicoes_valida():
    return TransacaoValida.query.all()


def incluir_transicao_valida(parametros):
    transicaoValida = TransacaoValida(**parametros)
    transicaoValida.id_transicao = None
    db.session.add(transicaoValida)
    db.session.commit()
    return transicaoValida.id_transicao

def remover_transicao_valida(id_transicao):
    db.session.query(TransacaoValida).filter(
        TransacaoValida.id_transicao == id_transicao).delete()
    db.session.commit()

def atualizar_transicao_valida(data_json):
    try:
        obj_db = TransacaoValida.query.filter(TransacaoValida.id_transicao == int(data_json['id_transicao'])).one()
    
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
        
                
        
        return Response(json.dumps({'message':'Situacao com id {} atualizada.'.format(obj_db.id_transicao)}), status=200)


def listar_transicoes_grupo_valida():
    return TransicaoGrupoValida.query.all()

def incluir_transicao_grupo_valida(parametros):
    transicaoValida = TransicaoGrupoValida(**parametros)
    transicaoValida.id_transicao_grp = None
    db.session.add(transicaoValida)
    db.session.commit()
    return transicaoValida.id_transicao_grp

def remover_transicao_grupo_valida(id_transicao_grp):
    db.session.query(TransicaoGrupoValida).filter(
        TransicaoGrupoValida.id_transicao_grp == id_transicao_grp).delete()
    db.session.commit()


def atualizar_transicao_valida(data_json):
    try:
        obj_db = TransicaoGrupoValida.query.filter(TransicaoGrupoValida.id_transicao_grp == int(data_json['id_transicao_grp'])).one()
    
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
        
                
        
        return Response(json.dumps({'message':'Situacao com id {} atualizada.'.format(obj_db.id_transicao_grp)}), status=200)

