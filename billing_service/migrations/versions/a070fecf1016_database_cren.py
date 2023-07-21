"""Database cren

Revision ID: a070fecf1016
Revises:
Create Date: 2023-07-05 22:42:03.424550

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import DDL
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID

from migrations.data.subscriptions import insert_subscription

from migrations.data.subscription_types import insert_subscription_type

from migrations.data.payments import insert_payment
from sql_app.sql import (
    drop_subscription_history_trigger,
    drop_payment_history_trigger,
    drop_subscription_type_history_trigger,
    drop_refund_history_trigger,
    drop_subscription_history_func,
    drop_payment_history_func,
    drop_subscription_type_history_func,
    drop_refund_history_func,
    subscription_history_func,
    subscription_type_history_func,
    payment_history_func,
    refund_history_func,
    subscription_history_trigger,
    subscription_type_history_trigger,
    payment_history_trigger,
    refund_history_trigger
)

revision = 'a070fecf1016'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    create_extension = DDL('''
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    ''')
    create_extension(target=None, bind=op.get_bind())

    op.create_table(
        'subscription',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('user_id', UUID(as_uuid=True)),
        sa.Column('start_date', sa.TIMESTAMP(), default=func.now()),
        sa.Column('end_date', sa.TIMESTAMP()),
        sa.Column('subscription_type_id', UUID(as_uuid=True), nullable=True),
        sa.Column('is_active', sa.BOOLEAN()),
        sa.Column('is_repeatable', sa.BOOLEAN()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'payment',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('subscription_id', UUID(as_uuid=True), nullable=False),
        sa.Column('payment_amount', sa.DECIMAL(precision=None), nullable=False),
        sa.Column('payment_status', sa.String(50), nullable=True),
        sa.Column('payment_date', sa.TIMESTAMP(), nullable=False),
        sa.Column('payment_method_id', sa.String(50), nullable=False),
        sa.ForeignKeyConstraint(['subscription_id'], ['subscription.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'subscription_type',
        sa.Column('id', UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('amount', sa.DECIMAL(), nullable=False),
        sa.Column('is_active', sa.BOOLEAN(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'refund',
        sa.Column('id', UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('refund_amount', sa.DECIMAL(precision=None), nullable=False),
        sa.Column('refund_status', sa.String(50), nullable=False),
        sa.Column('refund_date', sa.TIMESTAMP(), nullable=False),
        sa.Column('external_refund_id', sa.String(50), nullable=False),
        sa.Column('subscription_id', UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'subscription_history',
        sa.Column('id', UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), nullable=True),
        sa.Column('start_date', sa.TIMESTAMP(), default=func.now()),
        sa.Column('end_date', sa.TIMESTAMP()),
        sa.Column('subscription_type_id', UUID(as_uuid=True), nullable=True),
        sa.Column('is_active', sa.BOOLEAN()),
        sa.Column('is_repeatable', sa.BOOLEAN()),
        sa.Column('operation_date', sa.TIMESTAMP(), nullable=False),
        sa.Column('operation_type', sa.String(50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'payment_history',
        sa.Column('id', UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('subscription_id', UUID(as_uuid=True), nullable=False),
        sa.Column('payment_amount', sa.DECIMAL(precision=None), nullable=False),
        sa.Column('payment_status', sa.String(50), nullable=True),
        sa.Column('payment_method_id', sa.String(50), nullable=False),
        sa.Column('payment_date', sa.TIMESTAMP(), nullable=False),
        sa.Column('operation_date', sa.TIMESTAMP(), nullable=False),
        sa.Column('operation_type', sa.String(1), nullable=False),
        sa.ForeignKeyConstraint(['subscription_id'], ['subscription.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'subscription_type_history',
        sa.Column('id', UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('amount', sa.DECIMAL(precision=None), nullable=False),
        sa.Column('is_active', sa.BOOLEAN(), nullable=False),
        sa.Column('operation_date', sa.TIMESTAMP(), nullable=False),
        sa.Column('operation_type', sa.String(1), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'refund_history',
        sa.Column('id', UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('refund_amount', UUID(as_uuid=True), nullable=False),
        sa.Column('refund_status', sa.String(50), nullable=False),
        sa.Column('external_refund_id', sa.String(50), nullable=False),
        sa.Column('refund_date', sa.TIMESTAMP(), nullable=False),
        sa.Column('operation_date', sa.TIMESTAMP(), nullable=False),
        sa.Column('operation_type', sa.String(1), nullable=False),
        sa.Column('subscription_id', UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['subscription_id'], ['subscription.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.execute(insert_subscription)
    op.execute(insert_payment)
    op.execute(insert_subscription_type)
    op.execute(subscription_history_func)
    op.execute(subscription_type_history_func)
    op.execute(payment_history_func)
    op.execute(refund_history_func)
    op.execute(subscription_history_trigger)
    op.execute(subscription_type_history_trigger)
    op.execute(payment_history_trigger)
    op.execute(refund_history_trigger)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('refund')
    op.drop_table('subscription_type')
    op.drop_table('payment')
    op.drop_table('subscription')
    op.drop_table('refund_history')
    op.drop_table('subscription_type_history')
    op.drop_table('payment_history')
    op.drop_table('subscription_history')
    op.execute(drop_subscription_history_func)
    op.execute(drop_payment_history_func)
    op.execute(drop_subscription_type_history_func)
    op.execute(drop_refund_history_func)
    op.execute(drop_subscription_history_trigger)
    op.execute(drop_payment_history_trigger)
    op.execute(drop_subscription_type_history_trigger)
    op.execute(drop_refund_history_trigger)
    # ### end Alembic commands ###