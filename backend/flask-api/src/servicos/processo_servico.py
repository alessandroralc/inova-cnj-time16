import re
from ..entidades.modelo_fluxo import Processo
from ..persistencia.database import db


def inserir_processo(processo):
    db.session.add(processo)
    db.session.commit()


def retornar_processo(cd_processo):
    return db.session.query(Processo).filter(
        Processo.cd_processo == cd_processo).first()
