"""make_user_id_nullable

Revision ID: 4f6g7h8i9j0k
Revises: 22895d90d50a
Create Date: 2026-08-08 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f6g7h8i9j0k'
down_revision = '22895d90d50a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('conversations', 'user_id',
               existing_type=sa.VARCHAR(),
               nullable=True)


def downgrade() -> None:
    op.alter_column('conversations', 'user_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
