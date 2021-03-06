"""adding foreign keys

Revision ID: 98bf9e54d5c5
Revises: d75c0b5ca796
Create Date: 2021-11-24 17:32:51.243813

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null, table


# revision identifiers, used by Alembic.
revision = '98bf9e54d5c5'
down_revision = 'd75c0b5ca796'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
                        local_cols=['owner_id'], remote_cols =['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
