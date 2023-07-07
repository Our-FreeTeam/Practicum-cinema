from sqlalchemy import Table, MetaData, Column, ForeignKey, TIMESTAMP, func, String, BOOLEAN, DECIMAL, text
from sqlalchemy.dialects.postgresql import UUID


metadata = MetaData()

subscriptions = Table(
    "subscriptions",
    metadata,
    Column("id", UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column("person_id", UUID, ForeignKey('content.person.id', ondelete='CASCADE')),
    Column("start_date", TIMESTAMP, default=func.now()),
    Column("end_date", TIMESTAMP, nullable=False),
    Column("subscription_type", String, nullable=False),
    Column("is_active", BOOLEAN, nullable=False)
)

subscription_types = Table(
    "subscription_types",
    metadata,
    Column("id", UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column("name", String, nullable=False),
    Column("subscriptions_id", UUID, ForeignKey('subscriptions.id', ondelete='CASCADE')),
    Column("refund_amount", DECIMAL(precision=None), nullable=False),
    Column("is_active", BOOLEAN, nullable=False),
)

payments = Table(
    "payments",
    metadata,
    Column("id", UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column("person_id", UUID, ForeignKey('content.person.id', ondelete='CASCADE')),
    Column("subscriptions_id", UUID, ForeignKey('subscriptions.id', ondelete='CASCADE')),
    Column("payment_amount", DECIMAL(precision=None), nullable=False),
    Column("payment_status", String, nullable=False),
    Column("payment_method_id", String, nullable=False),
)

refunds = Table(
    "refunds",
    metadata,
    Column("id", UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column("payments_id", UUID, ForeignKey('payments.id', ondelete='CASCADE')),
    Column("refund_amount", UUID, ForeignKey('subscriptions.id', ondelete='CASCADE')),
    Column("payment_amount", DECIMAL(precision=None), nullable=False),
    Column("refund_status", String, nullable=False),
    Column("external_refund_id", String, nullable=False),
)

subscriptions_history = Table(
    "subscriptions_history",
    metadata,
    Column("id", UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column("person_id", UUID, ForeignKey('content.person.id', ondelete='CASCADE')),
    Column("start_date", TIMESTAMP, nullable=False),
    Column("end_date", TIMESTAMP, nullable=False),
    Column("subscription_type", String, nullable=False),
    Column("is_active", BOOLEAN, nullable=False),
    Column("operation_date", TIMESTAMP, nullable=False),
    Column("operation_type", String, nullable=False)
)

subscription_types_history = Table(
    "subscription_types_history",
    metadata,
    Column("id", UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column("name", String, nullable=False),
    Column("subscriptions_id", UUID, ForeignKey('subscriptions.id', ondelete='CASCADE')),
    Column("refund_amount", DECIMAL(precision=None), nullable=False),
    Column("is_active", BOOLEAN, nullable=False),
)

payments_history = Table(
    "payments_history",
    metadata,
    Column("id", UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column("person_id", UUID, ForeignKey('content.person.id', ondelete='CASCADE')),
    Column("subscriptions_id", UUID, ForeignKey('subscriptions.id', ondelete='CASCADE')),
    Column("payment_amount", DECIMAL(precision=None), nullable=False),
    Column("payment_status", String, nullable=False),
    Column("payment_method_id", String, nullable=False),
)

refunds_history = Table(
    "refunds_history",
    metadata,
    Column("id", UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column("payments_id", UUID, ForeignKey('payments.id', ondelete='CASCADE')),
    Column("refund_amount", UUID, ForeignKey('subscriptions.id', ondelete='CASCADE')),
    Column("payment_amount", DECIMAL(precision=None), nullable=False),
    Column("refund_status", String, nullable=False),
    Column("external_refund_id", String, nullable=False),
)
