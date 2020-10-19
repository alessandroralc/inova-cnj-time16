import re
from ..entidades.modelo_fluxo import Evento
from ..persistencia.database import db


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