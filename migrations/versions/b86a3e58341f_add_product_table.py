"""Add Product Table

Revision ID: b86a3e58341f
Revises: 
Create Date: 2026-11-24 15:00:13.617401

"""
from sqlalchemy import Column, INTEGER, VARCHAR, NVARCHAR, TIMESTAMP
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b86a3e58341f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # create new table
    op.create_table(  
    "products",  
    Column("id", sa.INTEGER, primary_key=True),  
    Column("name", sa.VARCHAR(50), nullable=False),  
    Column("description", sa.VARCHAR(200)),  
    Column("timestamp", sa.TIMESTAMP,
    Column("stock", sa.Integer,)
     
))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("products")
