"""Change keymap model and add multibinds with model keybinds

Revision ID: 754494f5f540
Revises: e54893de5b11
Create Date: 2022-12-20 15:05:44.313027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '754494f5f540'
down_revision = 'e54893de5b11'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('keymaps', 'keybind')


def downgrade() -> None:
    pass
