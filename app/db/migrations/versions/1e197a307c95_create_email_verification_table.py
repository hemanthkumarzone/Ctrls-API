"""create email verification table

Revision ID: 1e197a307c95
Revises: a3581676b224
Create Date: 2026-05-20
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '1e197a307c95'
down_revision = 'a3581676b224'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "email_verifications",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=False),
            primary_key=True,
            nullable=False
        ),

        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=False),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False
        ),

        sa.Column(
            "verification_code",
            sa.String(length=6),
            nullable=False
        ),

        sa.Column(
            "is_used",
            sa.Boolean(),
            nullable=False,
            server_default="false"
        ),

        sa.Column(
            "expires_at",
            sa.DateTime(timezone=True),
            nullable=False
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()")
        )
    )


def downgrade():

    op.drop_table("email_verifications")