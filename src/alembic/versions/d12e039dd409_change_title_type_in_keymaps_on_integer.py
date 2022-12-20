"""Change title type in keymaps on integer

Revision ID: d12e039dd409
Revises: 
Create Date: 2022-12-20 11:25:07.679587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd12e039dd409'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('keymaps', 'title')
    op.add_column('keymaps',
                  sa.Column('title',
                            sa.Integer,
                            comment='title of keymap'))


def downgrade() -> None:
    pass
