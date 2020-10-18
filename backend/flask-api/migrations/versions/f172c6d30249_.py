"""Ajustando campos not null da tb_hist_situacao para null

Revision ID: f172c6d30249
Revises: 2373796f9e26
Create Date: 2020-10-18 17:18:24.491127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f172c6d30249'
down_revision = '2373796f9e26'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("alter table tb_hist_situacao drop column id_situacao_origem")
    op.execute("alter table tb_hist_situacao drop column id_evento")
    op.execute("alter table tb_hist_situacao add column id_situacao_origem int4 null")
    op.execute("alter table tb_hist_situacao add column id_evento int4 null")    


def downgrade():
    pass
