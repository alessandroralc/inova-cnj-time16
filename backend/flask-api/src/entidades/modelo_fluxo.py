from sqlalchemy.orm import relationship
from ..persistencia.database import db


class Evento(db.Model):
    __tablename__ = 'tb_desc_evento'

    id_evento = db.Column(db.Integer, primary_key=True)
    ds_evento = db.Column(db.String(255), nullable=False)
    cd_evento = db.Column(db.String(30), nullable=False)
    ind_fluxo_ri = db.Column(db.String(1), nullable=False)
    ind_tipo_especial = db.Column(db.String(1), nullable=True)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Movimento(db.Model):
    __tablename__ = 'tb_desc_movimento'

    id_movimento = db.Column(db.Integer, primary_key=True)
    cd_tpu_movimento = db.Column(db.String(50), nullable=False)
    id_evento = db.Column(db.Integer, db.ForeignKey(
        'tb_desc_evento.id_evento'), nullable=False)

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
    sg_tribunal = db.Column(db.String(30), nullable=False)
    sg_grau = db.Column(db.String(30), nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class GrupoSituacao(db.Model):
    __tablename__ = 'tb_desc_grp_situacao'

    id_grupo = db.Column(db.Integer, primary_key=True)
    ds_grupo = db.Column(db.String(255), nullable=False)
    cd_grupo = db.Column(db.String(50), nullable=False)
    sg_tribunal = db.Column(db.String(30), nullable=False)
    sg_grau = db.Column(db.String(30), nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class FluxoMovimentos(db.Model):
    __tablename__ = 'tb_fluxo'

    id_fluxo_movimento = db.Column(
        db.Integer, nullable=False, primary_key=True)
    id_situacao_origem = db.Column(db.Integer, db.ForeignKey(
        'tb_desc_situacao.id_situacao'), nullable=False)
    id_evento = db.Column(db.Integer, db.ForeignKey(
        'tb_desc_evento.id_evento'), nullable=False)
    id_situacao_destino = db.Column(db.Integer, db.ForeignKey(
        'tb_desc_situacao.id_situacao'), nullable=False)
    ind_consistente = db.Column(db.String(1), nullable=False)
    ind_efetiva = db.Column(db.String(1), nullable=False)
    ind_fluxo_ri = db.Column(db.String(1), nullable=False)
    id_grupo = db.Column(db.Integer, db.ForeignKey(
        'tb_desc_grp_situacao.id_grupo'), nullable=False)
    sg_tribunal = db.Column(db.String(30), nullable=False)
    sg_grau = db.Column(db.String(30), nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class HistoricoEvento(db.Model):
    __tablename__ = 'tb_hist_evento'

    id_hist_evento = db.Column(db.Integer, nullable=False, primary_key=True)
    cd_processo = db.Column(db.String(50), nullable=False)
    cd_classe_judicial = db.Column(db.String(20), nullable=False)
    id_evento = db.Column(db.Integer, db.ForeignKey(
        'tb_desc_evento.id_evento'), nullable=False)
    dt_ocorrencia = db.Column(db.DateTime, nullable=False)
    ind_ri = db.Column(db.String(1), nullable=False)
    nu_autuacao = db.Column(db.Integer, nullable=False)
    sg_tribunal = db.Column(db.String(30), nullable=False)
    sg_grau = db.Column(db.String(30), nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class HistoricoSituacao(db.Model):
    __tablename__ = 'tb_hist_situacao'

    id_hist_situacao = db.Column(db.Integer, nullable=False, primary_key=True)
    cd_processo = db.Column(db.String(100), nullable=False)
    cd_classe_judicial = db.Column(db.String(20), nullable=False)
    nu_autuacao = db.Column(db.Integer, nullable=False)
    nu_seq_evento = db.Column(db.Integer, nullable=False)
    id_situacao_origem = db.Column(db.Integer, db.ForeignKey(
        'tb_desc_situacao.id_situacao'), nullable=True)
    id_situacao_destino = db.Column(db.Integer, db.ForeignKey(
    'tb_desc_situacao.id_situacao'), nullable=False)
    id_evento = db.Column(db.Integer, db.ForeignKey(
    'tb_desc_evento.id_evento'), nullable=True)
    dt_ocorrencia = db.Column(db.DateTime, nullable=False)
    ind_valida = db.Column(db.String(1), nullable=False)
    ind_consistente = db.Column(db.String(1), nullable=False)
    ind_efetiva = db.Column(db.String(1), nullable=False)
    sg_tribunal = db.Column(db.String(30), nullable=False)
    sg_grau = db.Column(db.String(30), nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Complemento(db.Model):
    __tablename__ = 'tb_desc_complemento'

    id_complemento = db.Column(db.Integer, primary_key=True)
    cd_tpu_complemento = db.Column(db.String(50), nullable=False)
    vl_complemento = db.Column(db.String(400), nullable=False)
    id_movimento = db.Column(db.Integer, db.ForeignKey(
        'tb_desc_movimento.id_movimento'), nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Processo(db.Model):
    __tablename__ = 'tb_processo'

    cd_processo = db.Column(db.String(100), primary_key=True)
    nu_processo = db.Column(db.String(50), nullable=False)
    cd_classe = db.Column(db.String(50), nullable=False)
    cd_orgao_julgador = db.Column(db.String(50), nullable=False)
    ds_orgao_julgador = db.Column(db.String(4000), nullable=False)
    sg_tribunal = db.Column(db.String(30), nullable=False)
    sg_grau = db.Column(db.String(30), nullable=False)
    ind_presidencia = db.Column(db.String(1), nullable=False)
    dt_autuacao = db.Column(db.DateTime, nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class ProcessoEvento(db.Model):
    __tablename__ = 'tb_processo_evento'

    id_processo_evento = db.Column(db.Integer, primary_key=True)
    dt_ocorrencia = db.Column(db.DateTime, nullable=False)
    cd_processo = db.Column(db.String(100), db.ForeignKey(
        'tb_processo.cd_processo'), nullable=False)
    id_evento = db.Column(db.Integer, db.ForeignKey(
        'tb_desc_evento.id_evento'), nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
