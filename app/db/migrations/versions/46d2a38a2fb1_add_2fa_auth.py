"""add 2fa auth

Revision ID: 46d2a38a2fb1
Revises: 17158d1be5bd
Create Date: 2026-05-21 16:08:51.702530

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46d2a38a2fb1'
down_revision = '17158d1be5bd'
branch_labels = None
depends_on = None


def upgrade() -> None:

    # EMAIL VERIFICATIONS TABLE

    op.add_column(
        'email_verifications',
        sa.Column(
            'purpose',
            sa.String(length=50),
            nullable=False,
            server_default='signup'
        )
    )

    op.add_column(
        'email_verifications',
        sa.Column(
            'reset_token',
            sa.String(length=255),
            nullable=True
        )
    )

    op.add_column(
        'email_verifications',
        sa.Column(
            'ip_address',
            sa.String(length=100),
            nullable=True
        )
    )

    op.add_column(
        'email_verifications',
        sa.Column(
            'device_info',
            sa.String(length=255),
            nullable=True
        )
    )

    op.add_column(
        'email_verifications',
        sa.Column(
            'location',
            sa.String(length=255),
            nullable=True
        )
    )

    op.add_column(
        'email_verifications',
        sa.Column(
            'failed_attempts',
            sa.Integer(),
            nullable=False,
            server_default='0'
        )
    )

    op.add_column(
        'email_verifications',
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        )
    )

    op.create_index(
        'ix_email_verification_user_purpose',
        'email_verifications',
        ['user_id', 'purpose'],
        unique=False
    )

    op.create_index(
        op.f('ix_email_verifications_expires_at'),
        'email_verifications',
        ['expires_at'],
        unique=False
    )

    op.create_index(
        op.f('ix_email_verifications_purpose'),
        'email_verifications',
        ['purpose'],
        unique=False
    )

    op.create_index(
        op.f('ix_email_verifications_user_id'),
        'email_verifications',
        ['user_id'],
        unique=False
    )

    # USERS TABLE

    op.add_column(
        'users',
        sa.Column(
            'two_factor_enabled',
            sa.Boolean(),
            nullable=False,
            server_default='false'
        )
    )

    op.add_column(
        'users',
        sa.Column(
            'two_factor_secret',
            sa.String(length=255),
            nullable=True
        )
    )


def downgrade() -> None:

    op.drop_column('users', 'two_factor_secret')
    op.drop_column('users', 'two_factor_enabled')

    op.drop_index(
        op.f('ix_email_verifications_user_id'),
        table_name='email_verifications'
    )

    op.drop_index(
        op.f('ix_email_verifications_purpose'),
        table_name='email_verifications'
    )

    op.drop_index(
        op.f('ix_email_verifications_expires_at'),
        table_name='email_verifications'
    )

    op.drop_index(
        'ix_email_verification_user_purpose',
        table_name='email_verifications'
    )

    op.drop_column('email_verifications', 'updated_at')
    op.drop_column('email_verifications', 'failed_attempts')
    op.drop_column('email_verifications', 'location')
    op.drop_column('email_verifications', 'device_info')
    op.drop_column('email_verifications', 'ip_address')
    op.drop_column('email_verifications', 'reset_token')
    op.drop_column('email_verifications', 'purpose')