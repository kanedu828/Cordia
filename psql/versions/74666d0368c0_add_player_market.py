"""Add player market

Revision ID: 74666d0368c0
Revises: f22bd6cc0de9
Create Date: 2024-12-12 02:30:16.652110

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = "74666d0368c0"
down_revision: Union[str, None] = "f22bd6cc0de9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "market_item",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "discord_id",
            sa.BigInteger,
            sa.ForeignKey("player.discord_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "item_name",
            sa.String(50),
            nullable=False,
        ),
        sa.Column("price", sa.BigInteger, nullable=False),
        sa.Column("count", sa.BigInteger, nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("market_item")
