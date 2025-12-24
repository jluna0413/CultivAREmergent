"""add_coin_redemptions

Revision ID: 90b1adfa2848
Revises: 467f9053dd68
Create Date: 2023-10-27 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90b1adfa2848'
down_revision = '467f9053dd68'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('crypto_coin_redemptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('coin_serial', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('PENDING', 'ESCROW_CREATED', 'COMPLETED', 'DISPUTED', 'CANCELLED', name='redemptionstatus'), nullable=True),
    sa.Column('redeemed_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_crypto_coin_redemptions_coin_serial'), 'crypto_coin_redemptions', ['coin_serial'], unique=True)
    op.create_index(op.f('ix_crypto_coin_redemptions_id'), 'crypto_coin_redemptions', ['id'], unique=False)
    
    op.create_table('coin_redemption_escrows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('redemption_id', sa.Integer(), nullable=False),
    sa.Column('escrow_address', sa.String(), nullable=False),
    sa.Column('app_id', sa.Integer(), nullable=False),
    sa.Column('amount_held', sa.Float(), nullable=True),
    sa.Column('is_funded', sa.Boolean(), nullable=True),
    sa.Column('is_released', sa.Boolean(), nullable=True),
    sa.Column('is_refunded', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['redemption_id'], ['crypto_coin_redemptions.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('redemption_id')
    )
    op.create_index(op.f('ix_coin_redemption_escrows_id'), 'coin_redemption_escrows', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_coin_redemption_escrows_id'), table_name='coin_redemption_escrows')
    op.drop_table('coin_redemption_escrows')
    op.drop_index(op.f('ix_crypto_coin_redemptions_id'), table_name='crypto_coin_redemptions')
    op.drop_index(op.f('ix_crypto_coin_redemptions_coin_serial'), table_name='crypto_coin_redemptions')
    op.drop_table('crypto_coin_redemptions')
