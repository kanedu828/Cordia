"""Update string size for bonus and default value

Revision ID: fc62a17da53c
Revises: 5549b5703c86
Create Date: 2024-09-10 07:23:49.597665

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc62a17da53c'
down_revision: Union[str, None] = '5549b5703c86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'gear',
        'bonus',
        existing_type=sa.String(length=50),
        type_=sa.String(length=1024),
        existing_nullable=False,
        server_default=""
    )

def downgrade() -> None:
    op.alter_column(
        'gear',
        'bonus',
        existing_type=sa.String(length=1024),
        type_=sa.String(length=50),
        existing_nullable=False,
        server_default=""
    )