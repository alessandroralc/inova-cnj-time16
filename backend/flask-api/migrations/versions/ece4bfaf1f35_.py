"""correção do tipo id_fluxo_movimento da tabela tb_fluxo

Revision ID: ece4bfaf1f35
Revises: baf5b994c881
Create Date: 2020-10-19 14:18:01.432342

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ece4bfaf1f35'
down_revision = 'baf5b994c881'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('alter table sanjus.tb_fluxo alter column id_fluxo_movimento type int4 USING id_fluxo_movimento::integer')


def downgrade():
    pass
