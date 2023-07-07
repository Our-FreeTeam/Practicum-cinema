from sqlalchemy import Table, MetaData, Column, ForeignKey, TIMESTAMP, func, String, BOOLEAN, DECIMAL, text
from sqlalchemy.dialects.postgresql import UUID


metadata = MetaData()

subscription = Table(
    "subscription",
    metadata,
    Column("id", UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column("person_id", UUID, ForeignKey('content.person.id', ondelete='CASCADE')),
    Column("start_date", TIMESTAMP, default=func.now()),
    Column("end_date", TIMESTAMP, nullable=False),
    Column("subscription_type", String, nullable=False),
    Column("is_active", BOOLEAN, nullable=False),
    Column("payment_id", String, nullable=False),
)

subscription_type = Table(
    "subscription_type",
    metadata,
    Column("id", UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column("name", String, nullable=False),
    Column("subscription_id", UUID, ForeignKey('subscription.id', ondelete='CASCADE')),
    Column("refund_amount", DECIMAL(precision=None), nullable=False),
    Column("is_active", BOOLEAN, nullable=False),
)

payment = Table(
    "payment",
    metadata,
    Column("id", UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column("person_id", UUID, ForeignKey('content.person.id', ondelete='CASCADE')),
    Column("subscription_id", UUID, ForeignKey('subscription.id', ondelete='CASCADE')),
    Column("payment_amount", DECIMAL(precision=None), nullable=False),
    Column("payment_status", String, nullable=False),
    Column("payment_method_id", String, nullable=False),
)

refund = Table(
    "refund",
    metadata,
    Column("id", UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column("payment_id", UUID, ForeignKey('payment.id', ondelete='CASCADE')),
    Column("refund_amount", UUID, ForeignKey('subscription.id', ondelete='CASCADE')),
    Column("payment_amount", DECIMAL(precision=None), nullable=False),
    Column("refund_status", String, nullable=False),
    Column("external_refund_id", String, nullable=False),
)

subscription_history = Table(
    "subscription_history",
    metadata,
    Column("id", UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column("person_id", UUID, ForeignKey('content.person.id', ondelete='CASCADE')),
    Column("start_date", TIMESTAMP, nullable=False),
    Column("end_date", TIMESTAMP, nullable=False),
    Column("subscription_type", String, nullable=False),
    Column("is_active", BOOLEAN, nullable=False),
    Column("payment_id", String, nullable=False),
    Column("operation_date", TIMESTAMP, nullable=False),
    Column("operation_type", String, nullable=False)
)

subscription_type_history = Table(
    "subscription_type_history",
    metadata,
    Column("id", UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column("name", String, nullable=False),
    Column("subscription_id", UUID, ForeignKey('subscription.id', ondelete='CASCADE')),
    Column("refund_amount", DECIMAL(precision=None), nullable=False),
    Column("is_active", BOOLEAN, nullable=False),
    Column("operation_date", TIMESTAMP, nullable=False),
    Column("operation_type", String, nullable=False)
)

payment_history = Table(
    "payment_history",
    metadata,
    Column("id", UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column("person_id", UUID, ForeignKey('content.person.id', ondelete='CASCADE')),
    Column("subscription_id", UUID, ForeignKey('subscription.id', ondelete='CASCADE')),
    Column("payment_amount", DECIMAL(precision=None), nullable=False),
    Column("payment_status", String, nullable=False),
    Column("payment_method_id", String, nullable=False),
    Column("operation_date", TIMESTAMP, nullable=False),
    Column("operation_type", String, nullable=False)
)

refund_history = Table(
    "refund_history",
    metadata,
    Column("id", UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column("payment_id", UUID, ForeignKey('payment.id', ondelete='CASCADE')),
    Column("refund_amount", UUID, ForeignKey('subscription.id', ondelete='CASCADE')),
    Column("payment_amount", DECIMAL(precision=None), nullable=False),
    Column("refund_status", String, nullable=False),
    Column("external_refund_id", String, nullable=False),
    Column("operation_date", TIMESTAMP, nullable=False),
    Column("operation_type", String, nullable=False)
)
