"""newpost

Revision ID: c4be7be3fd08
Revises: 1cfed4fa2d9e
Create Date: 2020-11-20 15:52:41.917139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4be7be3fd08'
down_revision = '1cfed4fa2d9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.create_foreign_key(None, 'post', 'user', ['user_id'], ['id'])
    op.drop_column('post', 'author')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('author', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.create_foreign_key(None, 'post', 'user', ['author'], ['id'])
    # ### end Alembic commands ###
