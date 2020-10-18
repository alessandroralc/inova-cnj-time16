"""empty message

Revision ID: eee7e66ed6dd
Revises: e4211f5b6a65
Create Date: 2020-10-18 13:24:03.225494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eee7e66ed6dd'
down_revision = 'e4211f5b6a65'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("Alter table tb_processo_evento drop column dt_ocorrencia");
    op.execute("Alter table tb_hist_situacao drop column dt_ocorrencia");
    op.execute("Alter table tb_hist_evento drop column dt_ocorrencia");

    op.execute("Alter table tb_processo_evento add column dt_ocorrencia timestamp without time zone not null");
    op.execute("Alter table tb_hist_situacao add column dt_ocorrencia  timestamp without time zone not null");
    op.execute("Alter table tb_hist_evento add column dt_ocorrencia timestamp without time zone not null");


def downgrade():
    pass
