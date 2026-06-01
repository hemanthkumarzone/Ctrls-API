"""add is_verified to users

Revision ID: a3581676b224
Revises: 08fff15484dc
Create Date: 2026-05-20 11:42:53.234668

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3581676b224'
down_revision = '08fff15484dc'
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.add_column(
        "users",
        sa.Column(
            "is_verified",
            sa.Boolean(),
            nullable=False,
            server_default="false"
        )
    )


def downgrade() -> None:

    op.drop_column(
        "users",
        "is_verified"
    )