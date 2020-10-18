"""Alterando o mapeamento do evento CDESP

Revision ID: baf5b994c881
Revises: f172c6d30249
Create Date: 2020-10-18 18:56:00.701478

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'baf5b994c881'
down_revision = 'f172c6d30249'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    update sanjus.tb_desc_movimento
    set id_evento = (select id_evento from sanjus.tb_desc_evento where cd_evento = 'CDESP')
    where cd_tpu_movimento = '51'    
    """)


def downgrade():
    pass
