"""Rebuild columns image_id and description

Revision ID: ac012a4bf9c7
Revises: 352b79a2f3ba
Create Date: 2024-07-19 13:34:50.448086

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ac012a4bf9c7'
down_revision: Union[str, None] = '352b79a2f3ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('hotels', 'services',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               nullable=True)
    op.alter_column('hotels', 'image_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('rooms', 'services',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               nullable=True)
    op.alter_column('rooms', 'image_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rooms', 'image_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('rooms', 'services',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               nullable=False)
    op.alter_column('hotels', 'image_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('hotels', 'services',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               nullable=False)
    # ### end Alembic commands ###
