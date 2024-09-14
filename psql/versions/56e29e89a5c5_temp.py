"""temp

Revision ID: 56e29e89a5c5
Revises: 5549b5703c86
Create Date: 2024-09-14 18:00:05.337815

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = '56e29e89a5c5'
down_revision: Union[str, None] = '5549b5703c86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add "trophies" column to "player" table
    op.add_column(
        "player",
        sa.Column("trophies", sa.Integer, nullable=False, server_default="0")
    )

    # Create "daily_leaderboard" table
    op.create_table(
        "daily_leaderboard",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "discord_id",
            sa.BigInteger,
            sa.ForeignKey("player.discord_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("exp", sa.Integer, nullable=False, server_default="0"),
        sa.Column("gold", sa.Integer, nullable=False, server_default="0"),
        sa.Column("monsters_killed", sa.Integer, nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
        sa.Column(
            "date",
            sa.Date,
            nullable=False,
            server_default=func.current_date()
        ),
        sa.UniqueConstraint("discord_id", "date", name="uq_discord_id_date")
    )


def downgrade() -> None:
    # Drop "daily_leaderboard" table
    op.drop_table("daily_leaderboard")

    # Remove "trophies" column from "player" table
    op.drop_column("player", "trophies")