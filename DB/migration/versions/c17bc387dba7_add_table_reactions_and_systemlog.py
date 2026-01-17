"""Add table Reactions and SystemLog

Revision ID: c17bc387dba7
Revises: 7e9670d9efdf
Create Date: 2026-01-08 22:49:16.894300

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c17bc387dba7'
down_revision: Union[str, Sequence[str], None] = '7e9670d9efdf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('system_log',
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('is_alert', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reactions',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('reaction_type', sa.Enum('FIRE', 'CRINGE', name='reactionstypes'), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('reactions')
    op.drop_table('system_log')
    op.execute("DROP TYPE reactionstypes")
