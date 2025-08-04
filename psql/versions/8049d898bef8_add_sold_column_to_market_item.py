"""add_sold_column_to_market_item

Revision ID: 8049d898bef8
Revises: 2929ae14d97e
Create Date: 2025-08-04 02:17:14.978993

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8049d898bef8'
down_revision: Union[str, None] = '2929ae14d97e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add sold column to market_item table
    op.add_column('market_item', sa.Column('sold', sa.Boolean, nullable=False, server_default='false'))


def downgrade() -> None:
    # Remove sold column from market_item table
    op.drop_column('market_item', 'sold')
