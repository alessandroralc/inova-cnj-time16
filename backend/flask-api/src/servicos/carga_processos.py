import os
from datetime import datetime
from elasticsearch import Elasticsearch
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ..persistencia.database import db
from src.entidades.modelo_fluxo import Processo
from . import processo_servico
from ..celery.celery_init import celery


COD_OJ_PRES = 72819


def pesquisa_com_processo(sigla_tribunal, grau, processo, start, end):
  return {
        "from" : start, "size" : end,
          "query": {"bool": {
              "should": [
                    {
                        "bool": {
                            "must": [
                                {
                                    "term": {"siglaTribunal.keyword": sigla_tribunal}
                                },
                                {
                                    "term": {"grau.keyword": grau}
                                },
                                {
                                    "term": {"_id": processo if processo else '*'}
                                }
                            ]
                        }
                    }]
          }}
      }


def pequisa_sem_processo(sigla_tribunal, grau, start, end):
  return {
        "from" : start, "size" : end,
          "query": {"bool": {
              "should": [
                    {
                        "bool": {
                            "must": [
                                {
                                    "term": {"siglaTribunal.keyword": sigla_tribunal}
                                },
                                {
                                    "term": {"grau.keyword": grau}
                                }
                            ]
                        }
                    }]
          }}
      }


def pesquisar_processos_elastic(siglaTribunal, grau, start, end, processo = None):
  es = Elasticsearch([{'host': os.getenv('HOST_ELASTIC'), 'port': os.getenv('PORT_ELASTIC')}],
                      http_auth=(os.getenv('USER_ELASTIC'), os.getenv('PASS_ELASTIC')))
  response = es.search(
      index="datajud_jt",
      body= pesquisa_com_processo(siglaTribunal, grau, processo, start, end) if processo else pequisa_sem_processo(siglaTribunal, grau, start, end)
  )
  return response


def retornar_processo(cd_processo):
    return processo_servico.retornar_processo(cd_processo)


def persistir_processo(processo):
  if retornar_processo(processo.cd_processo) is None:  
    processo_servico.inserir_processo(processo)    


def carregar_processo(registro):
  return Processo(
      cd_processo= registro['_id'],
      nu_processo= registro['_source']['dadosBasicos']['numero'],
      cd_classe= registro['_source']['dadosBasicos']['classeProcessual'],
      cd_orgao_julgador= registro['_source']['dadosBasicos']['orgaoJulgador']['codigoOrgao'],
      ds_orgao_julgador= registro['_source']['dadosBasicos']['orgaoJulgador']['nomeOrgao'],
      sg_tribunal= registro['_source']['siglaTribunal'],
      sg_grau= registro['_source']['grau'],
      dt_autuacao = datetime.strptime(registro['_source']['dadosBasicos']['dataAjuizamento'], '%Y%m%d%H%M%S'),
      ind_presidencia= 'S' if registro['_source']['dadosBasicos']['orgaoJulgador']['codigoOrgao'] == COD_OJ_PRES else 'N'
    )  


def existe_evento_processo(cd_processo, id_evento, dt_ocorrencia):
  with db.engine.connect() as conn:
    sql = """
      select id_processo_evento
      from tb_processo_evento
      where cd_processo = %s
      and id_evento = %s
      and dt_ocorrencia = %s
    """
    rs = conn.execute(sql, (cd_processo, id_evento, dt_ocorrencia))
    return  rs.fetchall()


def inserir_evento(cd_processo, id_evento, dt_ocorrencia):
  with db.engine.connect() as conn:
      resultado = existe_evento_processo(cd_processo, id_evento, dt_ocorrencia)
      if len(resultado) == 0:
        sql_insert = """Insert into tb_processo_evento values (nextval('tb_processo_evento_id_processo_evento_seq'), %s, %s, %s ) """
        conn.execute(sql_insert, (cd_processo, id_evento, dt_ocorrencia))


def carregar_movimento_sem_complemento(processo, mov, ind_tipo_especial):
  with db.engine.connect() as conn:
    sql = """
      select id_evento 
      from tb_desc_evento ev
      where 
      exists (select 1
      from tb_desc_movimento mov
      where mov.id_evento = ev.id_evento 
      and mov.cd_tpu_movimento = %s
      )
      and ind_tipo_especial = %s
    """
    result = conn.execute(sql, (str(mov['movimentoNacional']['codigoNacional']), ind_tipo_especial))
    for row in result:
      id_evento = row[0]
      dt_ocorrencia = datetime.strptime(mov['dataHora'], '%Y%m%d%H%M%S')
      inserir_evento(processo.cd_processo, id_evento, dt_ocorrencia)


def carregar_movimento_com_complemento(processo, mov, ind_tipo_especial):
  with db.engine.connect() as conn:
    sql = """
      select id_evento 
      from tb_desc_evento ev
      where 1 = 1
      {0}
      and ind_tipo_especial = %s
    """
    parametros = []
    sql_final = ""
    for comp in mov['complementoNacional']:
      sql_comp = """and exists
       (select 1
      from tb_desc_movimento mov
      join tb_desc_complemento comp on mov.id_movimento = comp.id_complemento
      where mov.id_evento = ev.id_evento 
      and mov.cd_tpu_movimento = %s
      and comp.cd_tpu_complemento = %s
      and comp.vl_complemento = %s
      )"""
      parametros.append(str(mov['movimentoNacional']['codigoNacional']))
      parametros.append(str(comp['codComplemento']))
      parametros.append(str(comp['codComplementoTabelado']))
      sql_final += sql_comp
    parametros.append(ind_tipo_especial)
    result = conn.execute(sql.format(sql_final), parametros)
    for row in result:
      id_evento = row[0]
      dt_ocorrencia = datetime.strptime(mov['dataHora'], '%Y%m%d%H%M%S')
      inserir_evento(processo.cd_processo, id_evento, dt_ocorrencia)


def carregar_eventos(processo, movimentos):
  for mov in movimentos:
    ind_tipo_especial = 'N'
    if mov.get('tipoDecisao'):
      ind_tipo_especial = 'M' if mov.get('tipoDecisao') == 0 else 'C'   
    ind_tipo_especial = processo.ind_presidencia if processo.ind_presidencia else ind_tipo_especial
    carregar_movimento_sem_complemento(processo, mov, ind_tipo_especial)


def limpar_dados(tribunal, instancia):
  print('Realizando limpeza dos dados')
  with db.engine.connect() as conn:
    sql = """delete from tb_processo_evento where cd_processo 
          in (select cd_processo from tb_processo where sg_tribunal = %s and sg_grau = %s)
          """
    conn.execute(sql, (tribunal, instancia))
    conn.execute('delete from tb_processo where sg_tribunal = %s and sg_grau = %s', (tribunal, instancia))
    conn.execute("""delete from tb_hist_situacao where cd_processo in 
                in (select cd_processo from tb_processo where sg_tribunal = %s and sg_grau = %s)
    """, (tribunal, instancia))


def limpar_dados_processo(tribunal, instancia, cd_processo):
  print('Realizando limpeza do processo')
  with db.engine.connect() as conn:
    sql = """delete from tb_processo_evento where cd_processo 
          in (select cd_processo from tb_processo where sg_tribunal = %s and sg_grau = %s and cd_processo = %s)
          """
    conn.execute(sql, (tribunal, instancia, cd_processo))
    conn.execute('delete from tb_processo where sg_tribunal = %s and sg_grau = %s and cd_processo = %s', (tribunal, instancia, cd_processo))
    conn.execute("""delete from tb_hist_situacao where cd_processo 
          in (select cd_processo from tb_processo where sg_tribunal = %s and sg_grau = %s and cd_processo = %s)
          """, (tribunal, instancia, cd_processo))


def carregar_historico_situacoes(cd_processo=None):
  with db.engine.connect() as conn:
    print(f'Validando as situações do processo {cd_processo}')
    conn.execute("""select fn_carga_tb_hist_situacao(%s)""", (cd_processo, ))    


@celery.task()
def carregar_dados_processos(tribunal, instancia, realizar_limpeza):
  print('Iniciando carga')
  if realizar_limpeza:
    limpar_dados(tribunal, instancia)
  total = pesquisar_processos_elastic(tribunal, instancia, 0, 1)['hits']['total']['value']
  tamanho_pag = 50 if total > 50 else total
  if tamanho_pag == 0:
    tamanho_pag = 1
  paginas = total / tamanho_pag
  resto = total % tamanho_pag
  reg_ini = 0
  reg_fim = tamanho_pag
  for i in range(0, round(paginas)):
    resp = pesquisar_processos_elastic(tribunal, instancia, reg_ini, reg_fim)
    for registro in resp['hits']['hits']:
      processo = carregar_processo(registro)
      persistir_processo(processo)
      carregar_eventos(processo, registro['_source']['movimento'])
    reg_ini += tamanho_pag
    reg_fim = (tamanho_pag + resto if i == paginas else tamanho_pag)
  carregar_historico_situacoes()
  print('Finalizada a carga')
    

@celery.task()
def carregar_dados_processo(tribunal, instancia, cd_processo):
  print(f'Iniciando a carga do processo {cd_processo}')
  limpar_dados_processo(tribunal, instancia, cd_processo)
  resp = pesquisar_processos_elastic(tribunal, instancia, 0, 1, cd_processo)
  for registro in resp['hits']['hits']:
    processo = carregar_processo(registro)
    print(f'Localizei o processo {processo.cd_processo}')
    persistir_processo(processo)
    carregar_eventos(processo, registro['_source']['movimento'])  
  carregar_historico_situacoes(cd_processo)
  print(f'Finalizada a carga do processo {cd_processo}')


if __name__ == "__main__":
    carregar_dados_processos('TRT3', 'G2')
