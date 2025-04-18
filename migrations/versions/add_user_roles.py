"""Add user roles

Revision ID: add_user_roles
Revises: add_transactions_and_oauth
Create Date: 2024-03-20 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_user_roles'
down_revision = 'add_transactions_and_oauth'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add role column to users table
    op.add_column('users', sa.Column('role', sa.String(20), nullable=False, server_default='user'))
    
    # Create index on role for faster queries
    op.create_index('idx_user_role', 'users', ['role'])

def downgrade() -> None:
    op.drop_index('idx_user_role', 'users')
    op.drop_column('users', 'role')