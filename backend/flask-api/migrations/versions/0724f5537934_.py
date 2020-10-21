"""Correção de default value para tb_fluxo.id_fluxo_movimento

Revision ID: 0724f5537934
Revises: dd4a73113bc6
Create Date: 2020-10-21 14:36:03.999160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0724f5537934'
down_revision = 'dd4a73113bc6'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("alter TABLE sanjus.tb_fluxo alter column id_fluxo_movimento set default nextval('sanjus.tb_fluxo_id_fluxo_seq')")


def downgrade():
    pass
