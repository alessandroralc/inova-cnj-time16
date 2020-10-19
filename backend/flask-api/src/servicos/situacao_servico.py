import re
from ..entidades.modelo_fluxo import Situacao
from ..persistencia.database import db


def listar_situacoes():
    return Situacao.query.all();
