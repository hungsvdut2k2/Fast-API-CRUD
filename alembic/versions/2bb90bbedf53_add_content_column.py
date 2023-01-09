"""add content column

Revision ID: 2bb90bbedf53
Revises: 8b1aa90ea104
Create Date: 2023-01-09 17:31:58.564980

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2bb90bbedf53"
down_revision = "8b1aa90ea104"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade():
    op.drop_column("posts", "content")
