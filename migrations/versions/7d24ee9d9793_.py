"""empty message

Revision ID: 7d24ee9d9793
Revises: None
Create Date: 2016-10-24 19:07:10.223742

"""

# revision identifiers, used by Alembic.
revision = '7d24ee9d9793'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('created_time', sa.Integer(), nullable=True),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    ### end Alembic commands ###