"""empty message

Revision ID: 9b53d96b641c
Revises: 6c891a84b11c
Create Date: 2021-07-09 12:57:08.128747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b53d96b641c'
down_revision = '6c891a84b11c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subreddits_keywords', schema=None) as batch_op:
        batch_op.drop_constraint('subreddits_keywords_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'subreddits', ['subreddit_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'keywords', ['keyword_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('users_subreddits', schema=None) as batch_op:
        batch_op.drop_constraint('users_subreddits_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('users_subreddits_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'subreddits', ['subreddit_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_subreddits', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('users_subreddits_ibfk_2', 'subreddits', ['subreddit_id'], ['id'])
        batch_op.create_foreign_key('users_subreddits_ibfk_1', 'users', ['user_id'], ['id'])

    with op.batch_alter_table('subreddits_keywords', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('subreddits_keywords_ibfk_2', 'keywords', ['keyword_id'], ['id'])

    # ### end Alembic commands ###