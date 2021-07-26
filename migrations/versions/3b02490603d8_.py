"""empty message

Revision ID: 3b02490603d8
Revises: 9b53d96b641c
Create Date: 2021-07-25 17:54:45.498017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b02490603d8'
down_revision = '9b53d96b641c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('monitoring')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('monitoring',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('users_id', sa.INTEGER(), nullable=True),
    sa.Column('subreddits_id', sa.INTEGER(), nullable=True),
    sa.Column('keywords_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['keywords_id'], ['keywords.id'], ),
    sa.ForeignKeyConstraint(['subreddits_id'], ['subreddits.id'], ),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###