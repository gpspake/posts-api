"""add names

Revision ID: 297240feaeff
Revises: 722007edc08a
Create Date: 2020-09-01 14:33:03.171161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '297240feaeff'
down_revision = '722007edc08a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('name', sa.Text(), nullable=True))
    op.add_column('tag', sa.Column('name', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tag', 'name')
    op.drop_column('post', 'name')
    # ### end Alembic commands ###
