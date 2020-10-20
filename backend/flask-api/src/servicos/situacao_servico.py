import re
from ..entidades.modelo_fluxo import Situacao, HistoricoSituacao, Evento, Processo
from ..persistencia.database import db
from sqlalchemy.orm import aliased,load_only,Load,with_expression


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


def construir_processo_fluxo(situacao):
    return {"nu_processo": situacao[0],
            "cd_classe": situacao[1],
            "cd_processo": situacao[2],
            "ds_situacao_origem": situacao[3],
            "ds_evento": situacao[4],
            "ds_situacao_destino": situacao[5],
            "dt_ocorrencia": situacao[6],
            "ind_consistente": situacao[7]}


def listar_processos_consistencia(str_consistente):
    SituacaoOrigem = aliased(Situacao)
    SituacaoDestino = aliased(Situacao)
    cursor = db.session.query(HistoricoSituacao, SituacaoOrigem, SituacaoDestino, Evento, Processo).\
    options(
        Load(Processo).load_only("nu_processo", "cd_classe","cd_processo"),
        Load(SituacaoOrigem).load_only("ds_situacao"),
        Load(Evento).load_only("ds_evento"),
        Load(SituacaoDestino).load_only("ds_situacao"),
        Load(HistoricoSituacao).load_only("dt_ocorrencia","ind_consistente")
    ).\
    join(SituacaoOrigem, HistoricoSituacao.id_situacao_origem == SituacaoOrigem.id_situacao).\
    join(SituacaoDestino, HistoricoSituacao.id_situacao_destino == SituacaoDestino.id_situacao).\
    join(Evento, HistoricoSituacao.id_evento == Evento.id_evento).\
    join(Processo, HistoricoSituacao.cd_processo == Processo.cd_processo).\
    filter(HistoricoSituacao.ind_consistente == str_consistente).\
    order_by(Processo.cd_processo, HistoricoSituacao.dt_ocorrencia).all()

    if cursor is not None:
        return cursor
    else:
        print('None')
        return []


def listar_fluxo_processo(id_processo):
    SituacaoOrigem = aliased(Situacao)
    SituacaoDestino = aliased(Situacao)
    cursor = db.session.query(HistoricoSituacao, SituacaoOrigem, SituacaoDestino, Evento, Processo).\
        options(
            Load(Processo).load_only("nu_processo", "cd_classe","cd_processo"),
            Load(SituacaoOrigem).load_only("ds_situacao"),
            Load(Evento).load_only("ds_evento"),
            Load(SituacaoDestino).load_only("ds_situacao"),
            Load(HistoricoSituacao).load_only("dt_ocorrencia","ind_consistente")
        ).\
        join(SituacaoOrigem, HistoricoSituacao.id_situacao_origem == SituacaoOrigem.id_situacao).\
        join(SituacaoDestino, HistoricoSituacao.id_situacao_destino == SituacaoDestino.id_situacao).\
        join(Evento, HistoricoSituacao.id_evento == Evento.id_evento).\
        join(Processo, HistoricoSituacao.cd_processo == Processo.cd_processo).\
        filter(HistoricoSituacao.cd_processo == id_processo).\
        order_by(HistoricoSituacao.dt_ocorrencia).all()
    if cursor is not None:
        return cursor
    else:
        return []
