"""Add strain_id aliases for backward compatibility (simple)

Revision ID: 2025_11_07_0301
Revises: 109317dd2a2f
Create Date: 2025-11-07 03:01:30.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2025_11_07_0301'
down_revision: Union[str, Sequence[str], None] = '109317dd2a2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add strain_id alias columns for backward compatibility
    # Add nullable strain_id column to plant table
    with op.batch_alter_table('plant', schema=None) as batch_op:
        batch_op.add_column(sa.Column('strain_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_plant_strain_id', 'cultivar', ['strain_id'], ['id'])

    # Add nullable strain_url column to plant table  
    with op.batch_alter_table('plant', schema=None) as batch_op:
        batch_op.add_column(sa.Column('strain_url', sa.String(length=255), nullable=True))

    # Backfill strain_id with current cultivar_id values
    op.execute("UPDATE plant SET strain_id = cultivar_id WHERE strain_id IS NULL")

    # Add nullable strain_name property support (for legacy access patterns)
    # Note: strain_name is typically a computed property, so no database column needed

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # Remove strain_id alias columns
    with op.batch_alter_table('plant', schema=None) as batch_op:
        batch_op.drop_constraint('fk_plant_strain_id', type_='foreignkey')
        batch_op.drop_column('strain_id')
        batch_op.drop_column('strain_url')

    # ### end Alembic commands ###