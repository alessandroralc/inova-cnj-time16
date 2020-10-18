"""Retirando complemento 5008

Revision ID: d77d5b7c3921
Revises: 495061e1bbe4
Create Date: 2020-10-18 14:28:57.319452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd77d5b7c3921'
down_revision = '495061e1bbe4'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("delete from tb_desc_complemento where cd_tpu_complemento in ('5008', '')")


def downgrade():
    pass
