"""create post table

Revision ID: 327b4e12336c
Revises: 
Create Date: 2021-11-24 15:19:03.162391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '327b4e12336c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', 
                    sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
