"""Atribuindo o movimento 123 para a evento RPI

Revision ID: 8194edcf5f47
Revises: d77d5b7c3921
Create Date: 2020-10-18 16:01:46.818068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8194edcf5f47'
down_revision = 'd77d5b7c3921'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""update tb_desc_movimento 
    set id_evento = (Select id_evento from tb_desc_evento where cd_evento = 'RPI') where cd_tpu_movimento = '123'
    """)


def downgrade():
    pass
