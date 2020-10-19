import re
from ..entidades.modelo_fluxo import FluxoMovimentos
from ..persistencia.database import db


def listar_fluxo(ind_fluxo_ri):
    return db.session.query(FluxoMovimentos).filter(FluxoMovimentos.ind_fluxo_ri == ind_fluxo_ri).all()
