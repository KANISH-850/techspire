"""Initial Unified HMS Schema

Revision ID: 001_initial_hms
Revises: 
Create Date: 2026-10-01 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial_hms'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. users
    op.create_table(
        'users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # 2. departments
    op.create_table(
        'departments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('budget', sa.Float(), nullable=True, server_default='0.0'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_departments_id'), 'departments', ['id'], unique=False)
    op.create_index(op.f('ix_departments_name'), 'departments', ['name'], unique=False)

    # 3. beds
    op.create_table(
        'beds',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=True),
        sa.Column('bed_number', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_beds_id'), 'beds', ['id'], unique=False)

    # 4. patients
    op.create_table(
        'patients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('gender', sa.String(), nullable=True),
        sa.Column('department_id', sa.Integer(), nullable=True),
        sa.Column('admission_date', sa.DateTime(), nullable=True),
        sa.Column('discharge_date', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('satisfaction_score', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_patients_id'), 'patients', ['id'], unique=False)
    op.create_index(op.f('ix_patients_name'), 'patients', ['name'], unique=False)

    # 5. admissions
    op.create_table(
        'admissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('patient_id', sa.Integer(), nullable=True),
        sa.Column('department_id', sa.Integer(), nullable=True),
        sa.Column('admission_date', sa.DateTime(), nullable=True),
        sa.Column('discharge_date', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admissions_id'), 'admissions', ['id'], unique=False)

    # 6. appointments
    op.create_table(
        'appointments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('patient_id', sa.Integer(), nullable=True),
        sa.Column('department_id', sa.Integer(), nullable=True),
        sa.Column('appointment_date', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_appointments_id'), 'appointments', ['id'], unique=False)

    # 7. transactions
    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=True),
        sa.Column('amount', sa.Float(), nullable=True),
        sa.Column('transaction_type', sa.String(), nullable=True),
        sa.Column('transaction_date', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transactions_id'), 'transactions', ['id'], unique=False)

    # 8. hospital_expenses
    op.create_table(
        'hospital_expenses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('amount', sa.Float(), nullable=True),
        sa.Column('expense_date', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_hospital_expenses_id'), 'hospital_expenses', ['id'], unique=False)

    # 9. alerts
    op.create_table(
        'alerts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('severity', sa.String(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('department_id', sa.Integer(), nullable=True),
        sa.Column('metric', sa.String(), nullable=True),
        sa.Column('value', sa.String(), nullable=True),
        sa.Column('threshold', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(), nullable=True, server_default='active'),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alerts_id'), 'alerts', ['id'], unique=False)

    # 10. vendors
    op.create_table(
        'vendors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('contact_person', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('average_delivery_days', sa.Integer(), nullable=True, server_default='5'),
        sa.Column('reliability_score', sa.Float(), nullable=True, server_default='100.0'),
        sa.Column('rating', sa.Float(), nullable=True, server_default='5.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vendors_id'), 'vendors', ['id'], unique=False)
    op.create_index(op.f('ix_vendors_name'), 'vendors', ['name'], unique=False)

    # 11. inventory_items
    op.create_table(
        'inventory_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('sku', sa.String(), nullable=True),
        sa.Column('batch_number', sa.String(), nullable=True),
        sa.Column('current_stock', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('minimum_stock', sa.Integer(), nullable=True, server_default='10'),
        sa.Column('maximum_stock', sa.Integer(), nullable=True, server_default='100'),
        sa.Column('daily_consumption', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('unit', sa.String(), nullable=True),
        sa.Column('unit_price', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('expiry_date', sa.Date(), nullable=True),
        sa.Column('vendor_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inventory_items_id'), 'inventory_items', ['id'], unique=False)
    op.create_index(op.f('ix_inventory_items_name'), 'inventory_items', ['name'], unique=False)
    op.create_index(op.f('ix_inventory_items_category'), 'inventory_items', ['category'], unique=False)
    op.create_index(op.f('ix_inventory_items_sku'), 'inventory_items', ['sku'], unique=True)

    # 12. purchase_orders
    op.create_table(
        'purchase_orders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('vendor_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(), nullable=True, server_default='Draft'),
        sa.Column('total_amount', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('expected_delivery_date', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_purchase_orders_id'), 'purchase_orders', ['id'], unique=False)

    # 13. purchase_order_items
    op.create_table(
        'purchase_order_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('purchase_order_id', sa.Integer(), nullable=True),
        sa.Column('inventory_item_id', sa.Integer(), nullable=True),
        sa.Column('quantity', sa.Integer(), nullable=True),
        sa.Column('unit_price', sa.Float(), nullable=True),
        sa.Column('total_price', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['inventory_item_id'], ['inventory_items.id'], ),
        sa.ForeignKeyConstraint(['purchase_order_id'], ['purchase_orders.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_purchase_order_items_id'), 'purchase_order_items', ['id'], unique=False)

    # 14. conversations
    op.create_table(
        'conversations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('session_id', sa.String(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_conversations_id'), 'conversations', ['id'], unique=False)
    op.create_index(op.f('ix_conversations_session_id'), 'conversations', ['session_id'], unique=False)

    # 15. messages
    op.create_table(
        'messages',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('conversation_id', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, server_default='sent'),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_id'), 'messages', ['id'], unique=False)
    op.create_index(op.f('ix_messages_conversation_id'), 'messages', ['conversation_id'], unique=False)
    op.create_index(op.f('ix_messages_role'), 'messages', ['role'], unique=False)


def downgrade() -> None:
    op.drop_table('messages')
    op.drop_table('conversations')
    op.drop_table('purchase_order_items')
    op.drop_table('purchase_orders')
    op.drop_table('inventory_items')
    op.drop_table('vendors')
    op.drop_table('alerts')
    op.drop_table('hospital_expenses')
    op.drop_table('transactions')
    op.drop_table('appointments')
    op.drop_table('admissions')
    op.drop_table('patients')
    op.drop_table('beds')
    op.drop_table('departments')
    op.drop_table('users')
