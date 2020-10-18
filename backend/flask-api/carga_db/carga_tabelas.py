import pandas as pd
from sqlalchemy import create_engine
engine = create_engine(
    'postgres://sanjus_app:inovacnj@time16-sanjus.ddns.net:5433/sanjus', echo=False)

df_situacao = pd.read_csv('carga_situacoes.csv', sep=',')
df_situacao['sg_tribunal'] = 'TRT3'
df_situacao['sg_grau'] = 'G2'
#df_situacao.to_sql('tb_desc_situacao', con=engine,
#                  if_exists='append', index=False)

df_eventos = pd.read_csv('carga_eventos_fluxo.csv', sep=',')
df_eventos.info()
df_eventos_sem_comp = df_eventos[df_eventos['cd_tipo_complemento'].isnull()]
df_eventos_sem_comp.head()


def verificar_registro(sql, cd_pesquisa):
    with engine.connect() as conn:
        result = conn.execute(sql, (cd_pesquisa, ))
        for row in result:
            return row['id']


def carga_complemento(registro, id_movimento):
    if registro['cd_tipo_complemento'] != 'NaN' and registro['ds_valor_complemento'] != 'NaN':
        sql = """Insert into tb_desc_complemento values (nextval('tb_desc_complemento_id_complemento_seq'),%s, %s, %s)                
        """
        with engine.connect() as conn:
            conn.execute(sql, (registro['cd_tipo_complemento'],
                               id_movimento, registro['ds_valor_complemento']))


def carga_movimento(registro, id_evento):
    id_movimento = verificar_registro(
        'select id_movimento as id from tb_desc_movimento where cd_tpu_movimento = %s', str(registro['cd_movimento']))
    if registro['cd_movimento'] != 'NaN' and id_movimento is None:
        sql = """Insert into tb_desc_movimento values (nextval('tb_desc_movimento_id_movimento_seq'), %s, %s)              
        """
        with engine.connect() as conn:
            conn.execute(sql, (registro['cd_movimento'], id_evento))
            id_movimento = verificar_registro(
                'select id_movimento as id from tb_desc_movimento where cd_tpu_movimento = %s', str(registro['cd_movimento']))
    return carga_complemento(registro, id_movimento)


def carga_evento(registro):
    id_evento = verificar_registro(
        'select id_evento as id from tb_desc_evento where cd_evento = %s', registro['cd_evento'])
    if id_evento is None:
        sql = """Insert into tb_desc_evento values (nextval('tb_desc_evento_id_evento_seq'), %s, %s, %s)              
        """
        with engine.connect() as conn:
            conn.execute(
                sql, (registro['ds_evento'], registro['ind_fluxo_ri'], registro['cd_evento']))
            id_evento = verificar_registro(
                'select id_evento as id from tb_desc_evento where cd_evento = %s', registro['cd_evento'])
    return carga_movimento(registro, id_evento)


#df_eventos.apply(carga_evento, axis=1)

df_grp_situacoes = pd.read_csv('carga_grp_situacoes.csv', sep=',')
df_grp_situacoes['sg_tribunal'] = 'TRT3'
df_grp_situacoes['sg_grau'] = 'G2'
#df_grp_situacoes.to_sql('tb_desc_grp_situacao', con=engine,
#                        if_exists='append', index=False)

df_fluxo = pd.read_csv('carga_fluxo.csv', sep=',')
df_fluxo['id_grp_situacao_origem'].fillna(9999.0, inplace=True)
df_fluxo = df_fluxo[df_fluxo['cd_evento'] != 'JSAM']


def carga_fluxo(registro):
    id_evento = verificar_registro(
        'select id_evento as id from tb_desc_evento where cd_evento = %s', registro['cd_evento'])
    sql = """Insert into tb_fluxo values (nextval('tb_fluxo_id_fluxo_seq'), %s, %s, %s, %s, %s, %s, %s, %s, %s)              
    """
    with engine.connect() as conn:
        conn.execute(sql, (registro['id_situacao_origem'], registro['id_situacao_destino'], registro['ind_consistente'],
                           registro['ind_efetiva'], registro['id_grp_situacao_origem'], 'G2', 'TRT3', id_evento, registro['ind_fluxo_ri']))


df_fluxo.apply(carga_fluxo, axis=1)
