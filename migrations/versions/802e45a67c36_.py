"""empty message

Revision ID: 802e45a67c36
Revises: 7d24ee9d9793
Create Date: 2016-10-24 23:31:01.204618

"""

# revision identifiers, used by Alembic.
revision = '802e45a67c36'
down_revision = '7d24ee9d9793'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blogcomments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=1000), nullable=True),
    sa.Column('created_time', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(length=1000), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('blog_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('blogs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=1000), nullable=True),
    sa.Column('created_time', sa.Integer(), nullable=True),
    sa.Column('updated_time', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('content', sa.String(length=1000), nullable=True),
    sa.Column('title', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blogs')
    op.drop_table('blogcomments')
    ### end Alembic commands ###