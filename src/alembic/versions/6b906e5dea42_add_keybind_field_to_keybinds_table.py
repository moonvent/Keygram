"""Add keybind field to keybinds table

Revision ID: 6b906e5dea42
Revises: 6da0cbd99857
Create Date: 2022-12-20 15:13:27.374737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b906e5dea42'
down_revision = '6da0cbd99857'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('keybinds',
                  sa.Column('keybind',
                            sa.String(16),
                            comment='keybind for this keymap'))


def downgrade() -> None:
    pass
