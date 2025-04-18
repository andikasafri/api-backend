"""Add transactions and OAuth support

Revision ID: add_transactions_and_oauth
Revises: initial_migration
Create Date: 2024-03-20 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_transactions_and_oauth'
down_revision = 'initial_migration'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add OAuth columns to users table
    op.add_column('users', sa.Column('oauth_provider', sa.String(50), nullable=True))
    op.add_column('users', sa.Column('oauth_id', sa.String(255), nullable=True))
    op.create_index('idx_oauth_id', 'users', ['oauth_provider', 'oauth_id'], unique=True)
    
    # Create transactions table
    op.create_table('transactions',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('total_amount', sa.Float, nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create transaction_items table for order details
    op.create_table('transaction_items',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('transaction_id', sa.String(36), sa.ForeignKey('transactions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('product_id', sa.String(36), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('price_at_time', sa.Float, nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('transaction_items')
    op.drop_table('transactions')
    op.drop_index('idx_oauth_id', 'users')
    op.drop_column('users', 'oauth_id')
    op.drop_column('users', 'oauth_provider')