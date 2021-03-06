"""new column user

Revision ID: 98e01a972dde
Revises: 7d4de137fc3d
Create Date: 2020-11-21 18:44:35.200047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98e01a972dde'
down_revision = '7d4de137fc3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('profil', sa.String(length=225), nullable=True))
    op.drop_column('user', 'profile')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('profile', sa.VARCHAR(length=225), nullable=True))
    op.drop_column('user', 'profil')
    # ### end Alembic commands ###
