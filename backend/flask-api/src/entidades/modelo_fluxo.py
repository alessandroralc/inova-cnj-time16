from sqlalchemy.orm import relationship
from ..persistencia.database import db


class Movimento(db.Model):
    __tablename__ = 'tb_desc_movimento'

    id_movimento = db.Column(db.Integer, primary_key=True)
    ds_movimento = db.Column(db.String(255), nullable=False)
    cd_tpu_movimento = db.Column(db.String(50), nullable=False)
    sg_movimento = db.Column(db.String(30), nullable=False)
    cd_tpu_complemento = db.Column(db.String(255), nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Situacao(db.Model):
    __tablename__ = 'tb_desc_situacao'

    id_situacao = db.Column(db.Integer, primary_key=True)
    ds_situacao = db.Column(db.String(255), nullable=False)
    cd_situacao = db.Column(db.String(50), nullable=False)
    ind_principal = db.Column(db.String(1), nullable=False)
    ind_ri = db.Column(db.String(1), nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class GrupoSituacao(db.Model):
    __tablename__ = 'tb_desc_grp_situacao'

    id_grupo = db.Column(db.Integer, primary_key=True)
    ds_grupo = db.Column(db.String(255), nullable=False)
    cd_grupo = db.Column(db.String(50), nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class FluxoMovimentos(db.Model):
    __tablename__ = 'tb_fluxo'

    id_fluxo_movimento = db.Column(db.String(255), nullable=False)
    id_situacao_origem = db.Column(db.Integer, db.ForeignKey(
        'tb_desc_situacao.id_situacao'), nullable=False)
    id_movimento = db.Column(db.Integer, db.ForeignKey(
        'tb_desc_movimento.id_movimento'), nullable=False)
    id_situacao_destino = db.Column(db.Integer, db.ForeignKey(
        'tb_desc_situacao.id_situacao'), nullable=False)
    ind_consistente = db.Column(db.String(1), nullable=False)
    ind_efetiva = db.Column(db.String(1), nullable=False)
    id_grupo = db.Column(db.Integer, db.ForeignKey(
        'tb_desc_grp_situacao.id_grupo'), nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
