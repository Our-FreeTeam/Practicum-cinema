from sqlalchemy import Table, MetaData, Column, ForeignKey, TIMESTAMP, func, String, BOOLEAN, DECIMAL, text
from sqlalchemy.dialects.postgresql import UUID


metadata = MetaData()

subscriptions = Table(
    "subscriptions",
    metadata,
    Column("id", UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column("person_id", UUID, ForeignKey('content.person.id', ondelete='CASCADE')),
    Column("start_date", TIMESTAMP, default=func.now()),
    Column("end_date", TIMESTAMP),
    Column("subscription_type", String, nullable=True),
    Column("is_active", BOOLEAN)
)

subscription_types = Table(
    "subscription_types",
    metadata,
    Column("id", UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column("name", String, nullable=False),
    Column("subscriptions_id", UUID, ForeignKey('subscriptions.id', ondelete='CASCADE')),
    Column("refund_amount", DECIMAL(precision=None)),
    Column("is_active", BOOLEAN),
)

payments = Table(
    "payments",
    metadata,
    Column("id", UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column("person_id", UUID, ForeignKey('content.person.id', ondelete='CASCADE')),
    Column("subscriptions_id", UUID, ForeignKey('subscriptions.id', ondelete='CASCADE')),
    Column("payment_amount", DECIMAL(precision=None)),
    Column("payment_status", String, nullable=True),
    Column("payment_method_id", String, nullable=False),
)

refunds = Table(
    "refunds",
    metadata,
    Column("id", UUID, primary_key=True, server_default=text('uuid_generate_v4()')),
    Column("payments_id", UUID, ForeignKey('payments.id', ondelete='CASCADE')),
    Column("refund_amount", UUID, ForeignKey('subscriptions.id', ondelete='CASCADE')),
    Column("payment_amount", DECIMAL(precision=None)),
    Column("refund_status", String, nullable=True),
    Column("external_refund_id", String, nullable=False),
)
