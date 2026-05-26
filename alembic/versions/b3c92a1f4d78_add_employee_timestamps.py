"""add employee timestamps

Revision ID: b3c92a1f4d78
Revises: ed5f1d5788cd
Create Date: 2026-05-26 14:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3c92a1f4d78'
down_revision: Union[str, Sequence[str], None] = 'ed5f1d5788cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add created_at and updated_at audit columns to the employees table.
    
    Both columns use server_default=now() so existing rows get a timestamp
    automatically without needing a data backfill.
    """
    op.add_column(
        'employees',
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.add_column(
        'employees',
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Drop timestamp columns — safe rollback with no data loss on other fields."""
    op.drop_column('employees', 'updated_at')
    op.drop_column('employees', 'created_at')
