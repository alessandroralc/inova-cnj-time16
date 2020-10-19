import re
from ..entidades.modelo_fluxo import Situacao
from ..persistencia.database import db


def incluir_situacao(parametros):
    situacao = Situacao(**parametros)
    situacao.id_situacao = None
    db.session.add(situacao)
    db.session.commit()
    return situacao.id_situacao


def remover_situacao(id_situacao):
    db.session.query(Situacao).filter(
        Situacao.id_situacao == id_situacao).delete()
    db.session.commit()


def listar_situacoes():
    return Situacao.query.all()


def listar_situacoes_filtro(cod_tribunal, cod_instancia):
    return db.session.query(Situacao).filter(Situacao.sg_tribunal == cod_tribunal and Situacao.sg_grau == cod_instancia).all()


def listar_situacoes_id(id_situacao):
    return db.session.query(Situacao).filter(Situacao.id_situacao == id_situacao).all()
