"""add stock column

Revision ID: 6d428a260736
Revises: b86a3e58341f
Create Date: 2026-11-25 12:20:19.383918

"""
from typing import Sequence, Union
from sqlalchemy import Column, INTEGER, VARCHAR, NVARCHAR, TIMESTAMP

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d428a260736'
down_revision: Union[str, Sequence[str], None] = 'b86a3e58341f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("products",sa.Column(
        "stock",sa.Integer,nullable=True
    ))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("products","stock")