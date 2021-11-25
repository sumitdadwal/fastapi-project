"""add content column in table for us

Revision ID: c3ae48992ec7
Revises: 327b4e12336c
Create Date: 2021-11-24 15:43:01.115421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3ae48992ec7'
down_revision = '327b4e12336c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
