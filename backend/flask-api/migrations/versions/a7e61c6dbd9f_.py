"""empty message

Revision ID: a7e61c6dbd9f
Revises: 306bb7fdd925
Create Date: 2020-10-17 21:49:34.086380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7e61c6dbd9f'
down_revision = '306bb7fdd925'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("insert into tb_desc_evento values (nextval('tb_desc_evento_id_evento_seq'), 'Distribuição para o relator', 'N', 'DRL')")
    op.execute("insert into tb_desc_evento values (nextval('tb_desc_evento_id_evento_seq'), 'Distribuição para o presidente', 'N', 'DPR')")
    op.execute("""
    insert into tb_desc_movimento
    select nextval('tb_desc_movimento_id_movimento_seq'), '26', id_evento
    from tb_desc_evento
    where cd_evento = 'DRL'
    """)
    pass


def downgrade():
    op.execute("delete from tb_desc_evento where cd_evento = 'DRL'")
    op.execute("delete from tb_desc_evento where cd_evento = 'DPR'")
    pass
