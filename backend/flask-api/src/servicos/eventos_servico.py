import re
from ..entidades.modelo_fluxo import Evento
from ..persistencia.database import db


def listar_eventos():
    return Evento.query.all();
