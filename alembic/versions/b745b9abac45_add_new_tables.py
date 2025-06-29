"""Add new tables

Revision ID: b745b9abac45
Revises: 6e19455f88f8
Create Date: 2025-06-06 15:32:14.878683

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b745b9abac45'
down_revision: Union[str, None] = '6e19455f88f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deterrence_permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('detection_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('allow', sa.Boolean(), nullable=True),
    sa.Column('issued_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('detection_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deterrence_permission')
    # ### end Alembic commands ###
