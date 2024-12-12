"""Change exp and gold to big int

Revision ID: 2929ae14d97e
Revises: 74666d0368c0
Create Date: 2024-12-12 07:12:09.451019

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2929ae14d97e'
down_revision: Union[str, None] = '74666d0368c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.alter_column(
        "player",
        "exp",
        existing_type=sa.Integer,
        type_=sa.BigInteger,
        existing_nullable=False,
        server_default="0",
    )
    op.alter_column(
        "player",
        "gold",
        existing_type=sa.Integer,
        type_=sa.BigInteger,
        existing_nullable=False,
        server_default="0",
    )

def downgrade() -> None:
    op.alter_column(
        "player",
        "exp",
        existing_type=sa.BigInteger,
        type_=sa.Integer,
        existing_nullable=False,
        server_default="0",
    )
    op.alter_column(
        "player",
        "gold",
        existing_type=sa.BigInteger,
        type_=sa.Integer,
        existing_nullable=False,
        server_default="0",
    )
