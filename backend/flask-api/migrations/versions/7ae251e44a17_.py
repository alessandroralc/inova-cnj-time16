"""Carga dos movimentos faltantes para representar os eventos

Revision ID: 7ae251e44a17
Revises: 3460854304e2
Create Date: 2020-10-18 08:23:54.534553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ae251e44a17'
down_revision = '3460854304e2'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    insert into tb_desc_movimento
    select nextval('tb_desc_movimento_id_movimento_seq'), '36', id_evento
    from tb_desc_evento
    where cd_evento = 'R'
    """)    
    op.execute("""
    insert into tb_desc_movimento
    select nextval('tb_desc_movimento_id_movimento_seq'), '10966', id_evento
    from tb_desc_evento
    where cd_evento = 'CONV'
    """)      
    op.execute("""
    insert into tb_desc_movimento
    select nextval('tb_desc_movimento_id_movimento_seq'), '26', id_evento
    from tb_desc_evento
    where cd_evento = 'DPR'
    """)         
    op.execute("""delete from tb_fluxo where id_evento = (select id_evento from tb_desc_evento where cd_evento = 'CRLR')""")
    op.execute("""delete from tb_desc_evento where cd_evento = 'CRLR'""")
    pass


def downgrade():
    pass
