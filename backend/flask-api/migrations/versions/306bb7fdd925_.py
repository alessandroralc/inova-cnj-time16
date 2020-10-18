"""empty message

Revision ID: 306bb7fdd925
Revises: 391c8106a2e4
Create Date: 2020-10-17 21:40:50.051902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '306bb7fdd925'
down_revision = '391c8106a2e4'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('create sequence tb_fluxo_id_fluxo_seq')
    pass

def downgrade():
    op.execute('drop sequence tb_fluxo_id_fluxo_seq')
    pass
