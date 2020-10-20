import re
from ..entidades.modelo_fluxo import Situacao, HistoricoSituacao, Evento, Processo
from ..persistencia.database import db
from sqlalchemy.orm import aliased


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


def listar_situacoes_grupo(id_grupo):
    return db.session.query(Situacao).filter(Situacao.id_grupo == id_grupo).all()


def listar_processos_consistencia(str_consistente):
    SituacaoOrigem = aliased(Situacao)
    SituacaoDestino = aliased(Situacao)
    db.session.query(HistoricoSituacao, SituacaoOrigem, SituacaoDestino, Evento, Processo).\
        with_entities(Processo.nu_processo, Processo.cd_classe, Processo.cd_processo, SituacaoOrigem.ds_situacao, Evento.ds_evento, SituacaoDestino.ds_situacao, HistoricoSituacao.dt_ocorrencia, HistoricoSituacao.ind_consistente).\
        join(SituacaoOrigem, HistoricoSituacao.id_situacao_origem == SituacaoOrigem.id_situacao).\
        join(SituacaoDestino, HistoricoSituacao.id_situacao_destino == SituacaoDestino.id_situacao).\
        join(Evento, HistoricoSituacao.id_evento == Evento.id_evento).\
        join(Processo, HistoricoSituacao.cd_processo == Processo.cd_processo).\
        filter(HistoricoSituacao.ind_consistente == str_consistente).\
        order_by(Processo.cd_processo, HistoricoSituacao.dt_ocorrencia).all()


def listar_fluxo_processo(id_processo):
    SituacaoOrigem = aliased(Situacao)
    SituacaoDestino = aliased(Situacao)
    db.session.query(HistoricoSituacao, SituacaoOrigem, SituacaoDestino, Evento, Processo).\
        with_entities(Processo.nu_processo, Processo.cd_classe, Processo.cd_processo, SituacaoOrigem.ds_situacao, Evento.ds_evento, SituacaoDestino.ds_situacao, HistoricoSituacao.dt_ocorrencia, HistoricoSituacao.ind_consistente).\
        join(SituacaoOrigem, HistoricoSituacao.id_situacao_origem == SituacaoOrigem.id_situacao).\
        join(SituacaoDestino, HistoricoSituacao.id_situacao_destino == SituacaoDestino.id_situacao).\
        join(Evento, HistoricoSituacao.id_evento == Evento.id_evento).\
        join(Processo, HistoricoSituacao.cd_processo == Processo.cd_processo).\
        filter(HistoricoSituacao.cd_processo == id_processo).\
        order_by(HistoricoSituacao.dt_ocorrencia).all()
