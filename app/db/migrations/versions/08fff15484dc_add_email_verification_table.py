"""add email verification table

Revision ID: 08fff15484dc
Revises: ff70f00498d6
Create Date: 2026-05-20

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '08fff15484dc'
down_revision = 'ff70f00498d6'
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        'email_verifications',

        sa.Column(
            'id',
            sa.UUID(),
            nullable=False
        ),

        sa.Column(
            'user_id',
            sa.UUID(),
            nullable=False
        ),

        sa.Column(
            'verification_code',
            sa.String(length=6),
            nullable=False
        ),

        sa.Column(
            'is_verified',
            sa.Boolean(),
            nullable=True
        ),

        sa.Column(
            'expires_at',
            sa.DateTime(timezone=True),
            nullable=False
        ),

        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            nullable=True
        ),

        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
        ),

        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:

    op.drop_table('email_verifications')