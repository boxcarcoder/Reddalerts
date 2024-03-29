"""empty message

Revision ID: 7572e10686d1
Revises: 1c5a67499fd1
Create Date: 2021-08-23 09:26:09.651953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7572e10686d1'
down_revision = '1c5a67499fd1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('received_posts', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_received_posts_received_post'), ['received_post'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('received_posts', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_received_posts_received_post'))

    # ### end Alembic commands ###
