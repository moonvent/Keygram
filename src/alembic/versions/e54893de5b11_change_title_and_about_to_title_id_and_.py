"""Change title and about to title_id and about_id to easy insternalization

Revision ID: e54893de5b11
Revises: d12e039dd409
Create Date: 2022-12-20 12:29:32.832138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e54893de5b11'
down_revision = 'd12e039dd409'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('keymaps', 'title')
    op.drop_column('keymaps', 'about')
    op.add_column('keymaps',
                  sa.Column('title_id',
                            sa.Integer,
                            comment='title_id of keymap which presented in src/database/keymaps.py'))


def downgrade() -> None:
    pass
