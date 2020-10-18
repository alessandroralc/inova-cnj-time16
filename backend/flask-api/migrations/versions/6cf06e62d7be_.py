"""Ajustando a tabela tb_hist_situacao

Revision ID: 6cf06e62d7be
Revises: 5463259131ec
Create Date: 2020-10-18 16:47:23.182129

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cf06e62d7be'
down_revision = '5463259131ec'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""alter table tb_hist_situacao drop column id_movimento """)


def downgrade():
    pass
