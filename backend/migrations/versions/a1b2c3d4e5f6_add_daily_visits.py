"""add daily_visits table

Revision ID: a1b2c3d4e5f6
Revises: 2bdbeee4663c
Create Date: 2026-03-17 21:00:00.000000
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "2bdbeee4663c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "daily_visits",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("date", sa.Date(), nullable=False, comment="统计日期"),
        sa.Column("count", sa.Integer(), nullable=False, server_default="0", comment="访问次数"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("date", name="uq_daily_visits_date"),
    )


def downgrade() -> None:
    op.drop_table("daily_visits")
