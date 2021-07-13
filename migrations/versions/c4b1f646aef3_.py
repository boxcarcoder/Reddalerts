"""empty message

Revision ID: c4b1f646aef3
Revises: 51adf011e82e
Create Date: 2021-07-08 14:36:57.906023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4b1f646aef3'
down_revision = '51adf011e82e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('submission_queue', sa.String(length=128), nullable=True))
        batch_op.create_index(batch_op.f('ix_users_submission_queue'), ['submission_queue'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_submission_queue'))
        batch_op.drop_column('submission_queue')

    # ### end Alembic commands ###