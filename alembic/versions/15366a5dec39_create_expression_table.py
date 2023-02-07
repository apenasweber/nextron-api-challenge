"""create expression table

Revision ID: 15366a5dec39
Revises: 
Create Date: 2023-02-06 08:34:05.441741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15366a5dec39'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'expression',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('expression', sa.String(256), nullable=False),
        sa.Column('result', sa.Float, nullable=False)
    )


def downgrade() -> None:
    pass
