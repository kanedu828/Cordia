"""Create initial tables

Revision ID: 5549b5703c86
Revises: 
Create Date: 2024-09-01 21:04:54.935814

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = "5549b5703c86"
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
        sa.Column("efficiency", sa.Integer, nullable=False, server_default="1"),
        sa.Column("luck", sa.Integer, nullable=False, server_default="1"),
        sa.Column("exp", sa.Integer, nullable=False, server_default="0"),
        sa.Column("gold", sa.Integer, nullable=False, server_default="0"),
        sa.Column("location", sa.String(256), server_default="the_plains_i"),
        sa.Column(
            "last_boss_killed",
            sa.TIMESTAMP(timezone=True),
            server_default=func.now() - sa.text("interval '24 hours'"),
        ),
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
        sa.Column(
            "last_idle_claim",
            sa.TIMESTAMP(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )

    op.create_table(
        "gear",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("discord_id", sa.BigInteger, nullable=False),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("stars", sa.Integer, server_default="0", nullable=False),
        sa.Column("bonus", sa.String(50), nullable=False, server_default="''"),
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
        sa.ForeignKeyConstraint(
            ["discord_id"], ["player.discord_id"], ondelete="CASCADE"
        ),
        sa.UniqueConstraint("discord_id", "name", name="uq_discord_id_name"),
    )

    op.create_table(
        "player_gear",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("discord_id", sa.BigInteger, nullable=False),
        sa.Column("gear_id", sa.Integer, nullable=False),
        sa.Column("slot", sa.String(50), nullable=False),
        sa.UniqueConstraint("discord_id", "slot", name="uix_player_gear_slot"),
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
        sa.ForeignKeyConstraint(
            ["discord_id"], ["player.discord_id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["gear_id"], ["gear.id"], ondelete="CASCADE"),
    ),

    op.create_table(
        "boss_instance",
        sa.Column("id", sa.Integer, autoincrement=True),
        sa.Column(
            "discord_id",
            sa.BigInteger,
            sa.ForeignKey("player.discord_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("current_hp", sa.Integer, nullable=False),
        sa.Column("name", sa.String(50), nullable=False),
        sa.PrimaryKeyConstraint("id", "discord_id"),
        sa.UniqueConstraint(
            "discord_id"
        ),  # This ensures discord_id is unique by itself
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
        sa.Column(
            "expiration_time",
            sa.TIMESTAMP(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )

    op.create_table(
        "item",
        sa.Column("discord_id", sa.BigInteger, sa.ForeignKey("player.discord_id", ondelete="CASCADE"), nullable=False),
        sa.Column("count", sa.Integer, nullable=False),
        sa.Column("name", sa.String(50), nullable=False),
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
        sa.PrimaryKeyConstraint("discord_id", "name")  # Composite primary key
    )


def downgrade() -> None:
    op.drop_table("player_gear")
    op.drop_table("gear")
    op.drop_table("player")
    op.drop_table("boss_instance")
    op.drop_table("item")
