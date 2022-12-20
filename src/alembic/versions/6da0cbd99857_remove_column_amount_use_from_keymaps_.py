"""Remove column amount use from keymaps and add this column to keybinds

Revision ID: 6da0cbd99857
Revises: 754494f5f540
Create Date: 2022-12-20 15:08:11.230278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6da0cbd99857'
down_revision = '754494f5f540'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('keymaps', 'amound_use')
    op.add_column('keybinds',
                  sa.Column('amount_use',
                            sa.Integer,
                            comment='amount use of this keybind'))


def downgrade() -> None:
    pass
