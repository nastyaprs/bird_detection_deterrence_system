"""initial

Revision ID: 1c379c5600da
Revises: 
Create Date: 2025-06-05 16:39:31.048071

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c379c5600da'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cameras',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('interface_type', sa.Text(), nullable=True),
    sa.Column('device_path', sa.Text(), nullable=True),
    sa.Column('model', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('deterrent_systems',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('type', sa.Text(), nullable=True),
    sa.Column('model', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.Text(), nullable=True),
    sa.Column('password_hash', sa.Text(), nullable=True),
    sa.Column('email', sa.Text(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('surname', sa.Text(), nullable=True),
    sa.Column('role', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('recorded_videos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('end_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('file_path', sa.Text(), nullable=True),
    sa.Column('camera_id', sa.Integer(), nullable=True),
    sa.Column('note', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['camera_id'], ['cameras.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bird_detections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
    sa.Column('video_id', sa.Integer(), nullable=True),
    sa.Column('confidence', sa.Float(), nullable=True),
    sa.Column('bird_lowest_amount', sa.Integer(), nullable=True),
    sa.Column('bird_highest_amount', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['video_id'], ['recorded_videos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('deterrence_actions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
    sa.Column('device_type', sa.Text(), nullable=True),
    sa.Column('action', sa.Text(), nullable=True),
    sa.Column('parameters', sa.JSON(), nullable=True),
    sa.Column('triggered_by', sa.Integer(), nullable=True),
    sa.Column('detection_id', sa.Integer(), nullable=True),
    sa.Column('deterrent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['detection_id'], ['bird_detections.id'], ),
    sa.ForeignKeyConstraint(['deterrent_id'], ['deterrent_systems.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deterrence_actions')
    op.drop_table('bird_detections')
    op.drop_table('recorded_videos')
    op.drop_table('users')
    op.drop_table('deterrent_systems')
    op.drop_table('cameras')
    # ### end Alembic commands ###
