id="w3z2uv"
"""upgrade auth security system

Revision ID: 5f546d0271e6
Revises: 1e197a307c95
Create Date: 2026-05-20

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers
revision = '5f546d0271e6'
down_revision = '1e197a307c95'
branch_labels = None
depends_on = None


from sqlalchemy import inspect


def upgrade():

    bind = op.get_bind()
    inspector = inspect(bind)

    # CHECK users table columns
    user_columns = [
        col["name"]
        for col in inspector.get_columns("users")
    ]

    # ADD is_verified ONLY IF NOT EXISTS
    if "is_verified" not in user_columns:

        op.add_column(
            "users",
            sa.Column(
                "is_verified",
                sa.Boolean(),
                nullable=False,
                server_default="false"
            )
        )

    # CHECK existing tables
    existing_tables = inspector.get_table_names()

    # CREATE email_verifications ONLY IF NOT EXISTS
    if "email_verifications" not in existing_tables:

        op.create_table(
            "email_verifications",

            sa.Column(
                "id",
                UUID(as_uuid=False),
                primary_key=True,
                nullable=False
            ),

            sa.Column(
                "user_id",
                UUID(as_uuid=False),
                sa.ForeignKey(
                    "users.id",
                    ondelete="CASCADE"
                ),
                nullable=False
            ),

            sa.Column(
                "verification_code",
                sa.String(length=6),
                nullable=False
            ),

            sa.Column(
                "purpose",
                sa.String(length=50),
                nullable=False,
                server_default="signup"
            ),

            sa.Column(
                "reset_token",
                sa.String(length=255),
                nullable=True
            ),

            sa.Column(
                "ip_address",
                sa.String(length=100),
                nullable=True
            ),

            sa.Column(
                "device_info",
                sa.String(length=255),
                nullable=True
            ),

            sa.Column(
                "location",
                sa.String(length=255),
                nullable=True
            ),

            sa.Column(
                "failed_attempts",
                sa.Integer(),
                nullable=False,
                server_default="0"
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
                nullable=False
            ),
        )