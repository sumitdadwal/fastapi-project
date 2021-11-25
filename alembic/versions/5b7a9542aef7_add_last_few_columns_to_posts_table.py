"""add last few columns to posts table

Revision ID: 5b7a9542aef7
Revises: 98bf9e54d5c5
Create Date: 2021-11-24 21:44:25.102295

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


# revision identifiers, used by Alembic.
revision = '5b7a9542aef7'
down_revision = '98bf9e54d5c5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
