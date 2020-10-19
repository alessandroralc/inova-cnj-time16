import re
from ..entidades.modelo_fluxo import GrupoSituacao
from ..persistencia.database import db


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
