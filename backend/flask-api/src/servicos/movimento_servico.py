import re
from ..entidades.modelo_fluxo import Movimento
from ..persistencia.database import db


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
