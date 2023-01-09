"""add entire vote table

Revision ID: 47aceea22eda
Revises: 4ce18c49d903
Create Date: 2023-01-09 17:36:54.708897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "47aceea22eda"
down_revision = "4ce18c49d903"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "votes",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "post_id"),
    )


def downgrade():
    op.drop_table("votes")
