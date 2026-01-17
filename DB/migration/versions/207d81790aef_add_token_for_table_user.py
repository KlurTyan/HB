"""Add token for table User

Revision ID: 207d81790aef
Revises: c17bc387dba7
Create Date: 2026-01-08 22:51:45.963229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '207d81790aef'
down_revision: Union[str, Sequence[str], None] = 'c17bc387dba7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('token', sa.String(length=255), nullable=True))
    op.create_unique_constraint(None, 'users', ['token'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'token')
