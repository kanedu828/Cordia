"""Create user table

Revision ID: 5549b5703c86
Revises: 
Create Date: 2024-09-01 21:04:54.935814

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5549b5703c86'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "player",
        sa.Column("discord_id", sa.BigInteger, primary_key=True),
        sa.Column("strength", sa.Integer, nullable=False, server_default="1"),
        sa.Column("persistence", sa.Integer, nullable=False, server_default="1"),
        sa.Column("intelligence", sa.Integer, nullable=False, server_default="1"),
        sa.Column("exp", sa.Integer, nullable=False, server_default="0"),
        sa.Column("gold", sa.Integer, nullable=False, server_default="0"),
        sa.Column("location", sa.String(256), server_default="The Plains")
    )


def downgrade() -> None:
    op.drop_table("player")
