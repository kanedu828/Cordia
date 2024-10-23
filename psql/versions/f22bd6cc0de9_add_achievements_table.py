"""Add achievements table

Revision ID: f22bd6cc0de9
Revises: 5549b5703c86
Create Date: 2024-10-22 22:55:00.444421

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = "f22bd6cc0de9"
down_revision: Union[str, None] = "5549b5703c86"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "achievement",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("discord_id", sa.BigInteger, nullable=False),
        sa.Column("monster", sa.String(256), nullable=False),
        sa.Column("count", sa.Integer, server_default="0", nullable=False),
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
        sa.UniqueConstraint("discord_id", "monster", name="uq_discord_id_monster"),
    )


def downgrade() -> None:
    op.drop_table("achievement")
