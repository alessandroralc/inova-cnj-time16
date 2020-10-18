"""Correção na tabela de complementos

Revision ID: 495061e1bbe4
Revises: eee7e66ed6dd
Create Date: 2020-10-18 14:15:47.807618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '495061e1bbe4'
down_revision = 'eee7e66ed6dd'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("delete from tb_desc_complemento where cd_tpu_complemento = 'NaN'")
    op.execute("update tb_desc_complemento set cd_tpu_complemento = replace(cd_tpu_complemento, '.0', '') ")
    op.execute("update tb_desc_complemento set vl_complemento = replace(vl_complemento, '.0', '') ")
    op.execute("delete from tb_desc_complemento where vl_complemento = 'NaN'")
    op.execute("delete from tb_desc_complemento where cd_tpu_complemento in ('5006','8', '5060', '28', '5014', '5023', '5071', '5061', '5011', '5000')")

def downgrade():
    pass
