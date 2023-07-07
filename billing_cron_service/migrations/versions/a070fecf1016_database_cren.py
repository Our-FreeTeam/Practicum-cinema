"""Database cren

Revision ID: a070fecf1016
Revises: 
Create Date: 2023-07-05 22:42:03.424550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import func
from sqlalchemy.dialects import postgresql

revision = 'a070fecf1016'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscriptions',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('person_id', postgresql.UUID(), nullable=True),
    sa.Column('start_date', sa.TIMESTAMP(), default=func.now()),
    sa.Column('end_date', sa.TIMESTAMP(), nullable=False),
    sa.Column('subscription_type', sa.String(), nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), nullable=False),
    sa.ForeignKeyConstraint(['person_id'], ['content.person.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('person_id', postgresql.UUID(), nullable=True),
    sa.Column('subscriptions_id', postgresql.UUID(), nullable=False),
    sa.Column('payment_amount', sa.DECIMAL(), nullable=True),
    sa.Column('payment_status', sa.String(), nullable=False),
    sa.Column('payment_method_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['person_id'], ['content.person.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['subscriptions_id'], ['subscriptions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subscription_types',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('subscriptions_id', postgresql.UUID(), nullable=True),
    sa.Column('refund_amount', sa.DECIMAL(), nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), nullable=False),
    sa.ForeignKeyConstraint(['subscriptions_id'], ['subscriptions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('refunds',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('payments_id', postgresql.UUID(), nullable=True),
    sa.Column('refund_amount', postgresql.UUID(), nullable=False),
    sa.Column('payment_amount', sa.DECIMAL(), nullable=False),
    sa.Column('refund_status', sa.String(), nullable=False),
    sa.Column('external_refund_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['payments_id'], ['payments.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['refund_amount'], ['subscriptions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subscriptions_history',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('person_id', postgresql.UUID(), nullable=True),
    sa.Column('start_date', sa.TIMESTAMP(), nullable=False),
    sa.Column('end_date', sa.TIMESTAMP(), nullable=False),
    sa.Column('subscription_type', sa.String(), nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), nullable=False),
    sa.Column('operation_date', sa.TIMESTAMP(), nullable=False),
    sa.Column('operation_type', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['person_id'], ['content.person.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments_history',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('person_id', postgresql.UUID(), nullable=True),
    sa.Column('subscriptions_id', postgresql.UUID(), nullable=False),
    sa.Column('payment_amount', sa.DECIMAL(), nullable=True),
    sa.Column('payment_status', sa.String(), nullable=False),
    sa.Column('payment_method_id', sa.String(), nullable=False),
    sa.Column('operation_date', sa.TIMESTAMP(), nullable=False),
    sa.Column('operation_type', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['person_id'], ['content.person.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['subscriptions_id'], ['subscriptions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subscription_types_history',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('subscriptions_id', postgresql.UUID(), nullable=True),
    sa.Column('refund_amount', sa.DECIMAL(), nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), nullable=False),
    sa.Column('operation_date', sa.TIMESTAMP(), nullable=False),
    sa.Column('operation_type', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['subscriptions_id'], ['subscriptions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('refunds_history',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('payments_id', postgresql.UUID(), nullable=True),
    sa.Column('refund_amount', postgresql.UUID(), nullable=False),
    sa.Column('payment_amount', sa.DECIMAL(), nullable=False),
    sa.Column('refund_status', sa.String(), nullable=False),
    sa.Column('external_refund_id', sa.String(), nullable=False),
    sa.Column('operation_date', sa.TIMESTAMP(), nullable=False),
    sa.Column('operation_type', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['payments_id'], ['payments.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['refund_amount'], ['subscriptions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('refunds')
    op.drop_table('subscription_types')
    op.drop_table('payments')
    op.drop_table('subscriptions')
    op.drop_table('refunds_history')
    op.drop_table('subscription_types_history')
    op.drop_table('payments_history')
    op.drop_table('subscriptions_history')
    # ### end Alembic commands ###