"""add new column datetime

Revision ID: e4aa5894557d
Revises: 3a51231d1885
Create Date: 2020-11-21 22:24:47.687712

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4aa5894557d'
down_revision = '3a51231d1885'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('create_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('update_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('update_at')
        batch_op.drop_column('create_at')

    # ### end Alembic commands ###