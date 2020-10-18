"""empty message

Revision ID: 3460854304e2
Revises: a7e61c6dbd9f
Create Date: 2020-10-17 22:05:40.819274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3460854304e2'
down_revision = 'a7e61c6dbd9f'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("insert into tb_desc_evento values (nextval('tb_desc_evento_id_evento_seq'), 'Retirado de Pauta', 'S', 'RP')")
    op.execute("insert into tb_desc_evento values (nextval('tb_desc_evento_id_evento_seq'), 'Sessão iniciada', 'S', 'SI')")
    op.execute("insert into tb_desc_evento values (nextval('tb_desc_evento_id_evento_seq'), 'Redistribuição', 'S', 'R')")
    op.execute("insert into tb_desc_evento values (nextval('tb_desc_evento_id_evento_seq'), 'Decisão colegiada interlocutória', 'S', 'DCI')")
    op.execute("insert into tb_desc_evento values (nextval('tb_desc_evento_id_evento_seq'), 'Restituições pelo relator para remessa ao MPT', 'N', 'RRLMPT')")
    op.execute("insert into tb_desc_evento values (nextval('tb_desc_evento_id_evento_seq'), 'Conversão de Classe - O', 'N', 'CONV')")
    op.execute("insert into tb_desc_evento values (nextval('tb_desc_evento_id_evento_seq'), 'Conclusão para relatar de recursos por distribuição (Provimento CGJT n.3/2015)', 'N', 'CRLR')")
    op.execute("insert into tb_desc_evento values (nextval('tb_desc_evento_id_evento_seq'), 'Recebimento do processo após envio ao MPT', 'N', 'RCBMPT')")
    pass


def downgrade():
    op.execute("delete from tb_desc_evento where cd_evento = 'RP'")
    op.execute("delete from tb_desc_evento where cd_evento = 'SI'")
    op.execute("delete from tb_desc_evento where cd_evento = 'R'")
    op.execute("delete from tb_desc_evento where cd_evento = 'DCI'")
    op.execute("delete from tb_desc_evento where cd_evento = 'RRLMPT'")
    op.execute("delete from tb_desc_evento where cd_evento = 'CONV'")
    op.execute("delete from tb_desc_evento where cd_evento = 'CRLR'")
    op.execute("delete from tb_desc_evento where cd_evento = 'RCBMPT'")
    pass