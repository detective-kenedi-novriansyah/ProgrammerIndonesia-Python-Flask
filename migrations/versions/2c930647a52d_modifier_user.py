"""modifier user

Revision ID: 2c930647a52d
Revises: c0046ded0583
Create Date: 2020-11-21 17:46:03.843282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c930647a52d'
down_revision = 'c0046ded0583'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('profile', sa.String(length=225), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'profile')
    # ### end Alembic commands ###