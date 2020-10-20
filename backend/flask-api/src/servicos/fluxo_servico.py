import re
from typing import Dict
from ..entidades.modelo_fluxo import FluxoMovimentos
from ..persistencia.database import db
import sys
from sqlalchemy.orm import aliased,load_only,Load,exc
from flask_restful import abort
from flask import  Response
import json


def incluir_fluxo(parametros):
    fluxo = FluxoMovimentos(**parametros)
    fluxo.id_fluxo = None
    db.session.add(fluxo)
    db.session.commit()
    return fluxo.id_fluxo


def remover_evento(id_fluxo):
    db.session.query(FluxoMovimentos).filter(
        FluxoMovimentos.id_fluxo == id_fluxo).delete()
    db.session.commit()


def listar_fluxo(ind_fluxo_ri):
    return db.session.query(FluxoMovimentos).filter(FluxoMovimentos.ind_fluxo_ri == ind_fluxo_ri).all()


def listar_fluxo_id(id_fluxo):
    return db.session.query(FluxoMovimentos).filter(FluxoMovimentos.id_fluxo_movimento == id_fluxo).all()


def listar_fluxo_filtro(ind_fluxo_ri, cd_tribunal, cd_grau):
    return db.session.query(FluxoMovimentos).filter(FluxoMovimentos.ind_fluxo_ri == ind_fluxo_ri
                                                    and FluxoMovimentos.sg_grau == cd_grau
                                                    and FluxoMovimentos.sg_tribunal == cd_tribunal).all()


def retornar_tribunais_com_fluxo():
    with db.engine.connect() as conn:
        sql = 'select distinct sg_tribunal from sanjus.tb_fluxo'
        rs = conn.execute(sql)
        return [{'sg_tribunal': row[0]} for row in rs]


def retornar_graus_com_fluxo(cd_tribunal):
    with db.engine.connect() as conn:
        sql = 'select distinct sg_grau from sanjus.tb_fluxo where sg_tribunal = %s'
        rs = conn.execute(sql, (cd_tribunal, ))
        return [{'sg_grau': row[0]} for row in rs]


def gerar_transicoes_rede(cd_tribunal, cd_instancia, ind_consistente):
    """Formato do json a ser gerado
    [
      {source: "Michael", target: "Amazon", type: "licensing"},
      {source: "Microsoft", target: "HTC", type: "licensing"},
      {source: "Samsung", target: "Apple", type: "suit"},
      {source: "Motorola", target: "Apple", type: "suit"},
      {source: "Nokia", target: "Apple", type: "resolved"},
      {source: "HTC", target: "Apple", type: "suit"}
    ]
    """
    with db.engine.connect() as conn:
        sql = """
        select stori.cd_situacao as cd_situacao_origem,
        stori.ds_situacao  as ds_situacao_origem,
        stdest.cd_situacao  as cd_situacao_dest,
        stdest.ds_situacao  as ds_situacao_dest,
        ev.cd_evento,
        ev.ds_evento 
        from sanjus.tb_fluxo fluxo
        join sanjus.tb_desc_situacao stori on fluxo.id_situacao_origem = stori.id_situacao
        join sanjus.tb_desc_situacao stdest on fluxo.id_situacao_destino = stdest.id_situacao 
        join sanjus.tb_desc_evento ev on (fluxo.id_evento = ev.id_evento)
        where fluxo.sg_grau = %s
        and fluxo.sg_tribunal = %s
        and fluxo.ind_consistente = %s    
        """
        rs = conn.execute(sql, (cd_instancia, cd_tribunal, ind_consistente))
        return [{'source_cd': row[0],
                 'source_ds': row[1],
                 'target_cd': row[2],
                 'target_ds': row[3],
                 'transition_cd': row[4],
                 'transition_ds': row[5]
                 } for row in rs]


def situacao_possui_filhos(cd_tribunal, cd_instancia, ind_consistente, id_situacao):
    with db.engine.connect() as conn:
        sql = """
        select count(*)
        from tb_fluxo fluxo
        where fluxo.sg_grau = %s
        and fluxo.sg_tribunal = %s
        and fluxo.ind_consistente = %s      
        and fluxo.id_situacao_origem = %s
        and fluxo.id_situacao_origem <> fluxo.id_situacao_destino
        """
        rs = conn.execute(sql, (cd_instancia, cd_tribunal,
                                ind_consistente, id_situacao))
        return rs.fetchall()


def recuperar_transicao_arvore(cd_tribunal, cd_instancia, ind_consistente, id_situacao=None):

    with db.engine.connect() as conn:
        sql = """
        select distinct 
        stdest.cd_situacao  as cd_situacao_dest,
        stdest.ds_situacao  as ds_situacao_dest,
        fluxo.id_situacao_destino,
        fluxo.id_situacao_origem
        from sanjus.tb_fluxo fluxo
        join sanjus.tb_desc_situacao stori on fluxo.id_situacao_origem = stori.id_situacao
        join sanjus.tb_desc_situacao stdest on fluxo.id_situacao_destino = stdest.id_situacao 
        join sanjus.tb_desc_evento ev on (fluxo.id_evento = ev.id_evento)
        where fluxo.sg_grau = %s
        and fluxo.sg_tribunal = %s
        and fluxo.ind_consistente = %s  
        {0}
        """
        valor_parametro = ''
        if id_situacao:
            sql = sql.format(
                "and fluxo.id_situacao_origem = %s and fluxo.id_situacao_origem <> fluxo.id_situacao_destino ")
            valor_parametro = id_situacao
        else:
            sql = sql.format("and stori.fl_inicio = %s")
            valor_parametro = 'S'
        rs = conn.execute(sql, (cd_instancia, cd_tribunal,
                                ind_consistente, valor_parametro))
        return rs.fetchall()


def gerar_transicoes_arvore(cd_tribunal, cd_instancia, ind_consistente):
    sys.setrecursionlimit(15000)

    transicoes_inicio = recuperar_transicao_arvore(
        cd_tribunal, cd_instancia, ind_consistente)
    id_inicio = transicoes_inicio[0][3]
    deep = 10
    return {'cd_situacao': 'I',
            'ds_situacao': 'Início', 
            'children': funcao_recursiva(cd_tribunal, cd_instancia,
                                         ind_consistente, id_inicio, None, deep, 1)
            }


def funcao_recursiva(cd_tribunal, cd_instancia, ind_consistente, id_situacao, linha, deep, nivel_atual):
    filhos = situacao_possui_filhos(
        cd_tribunal, cd_instancia, ind_consistente, id_situacao)

    if filhos[0][0] > 0 and nivel_atual <= deep:
        transicoes_destino = recuperar_transicao_arvore(
            cd_tribunal, cd_instancia, ind_consistente, id_situacao)
        lista = []
        for row in transicoes_destino:
            lista_filhos = funcao_recursiva(
                cd_tribunal, cd_instancia, ind_consistente, row[2], row, deep, nivel_atual+1)
            lista.append({'cd_situacao': row[0],
                          'ds_situacao': row[1],
                          'children': lista_filhos
                          })
        return lista
    else:
        return {'cd_situacao': linha[0],
                'ds_situacao': linha[1]
                }


def atualizar_fluxo(data_json):
    
    try:
        obj_db = FluxoMovimentos.query.filter(FluxoMovimentos.id_fluxo_movimento == int(data_json['id_fluxo_movimento'])).one()
    
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
        
                
        
        return Response(json.dumps({'message':'Situacao com id {} atualizada.'.format(obj_db.id_fluxo_movimento)}), status=200)
