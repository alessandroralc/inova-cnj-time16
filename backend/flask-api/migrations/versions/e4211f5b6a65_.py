"""Atualizando ind_tipo_especial para os casos sem tipo especial (N)

Revision ID: e4211f5b6a65
Revises: 6fdbb9233bd6
Create Date: 2020-10-18 12:47:05.177244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4211f5b6a65'
down_revision = '6fdbb9233bd6'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("update tb_desc_evento set ind_tipo_especial= 'N' where ind_tipo_especial is null")


def downgrade():
    pass
