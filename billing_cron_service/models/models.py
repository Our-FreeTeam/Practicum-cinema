from sqlalchemy import Table, MetaData, Column, ForeignKey, TIMESTAMP, func, String, BOOLEAN, DECIMAL
from sqlalchemy.dialects.postgresql import UUID


metadata = MetaData()

subscriptions = Table(
    "subscriptions",
    metadata,
    Column("user_id", UUID, ForeignKey('content.user.id', ondelete='CASCADE')),
    Column("start_date", TIMESTAMP, default=func.now()),
    Column("end_date", TIMESTAMP),
    Column("subscription_type", String, nullable=True),
    Column("is_active", BOOLEAN),
)

subscription_types = Table(
    "subscription_types",
    metadata,
    Column("name", String, nullable=False),
    Column("subscription_id", UUID, ForeignKey('content.subscription.id', ondelete='CASCADE')),
    Column("refund_amount", DECIMAL(precision=None)),
    Column("is_active", BOOLEAN),
)

payments = Table(
    "payments",
    metadata,
    Column("user_id", UUID, ForeignKey('content.user.id', ondelete='CASCADE')),
    Column("subscription_id", UUID, ForeignKey('content.subscription.id', ondelete='CASCADE')),
    Column("payment_amount", DECIMAL(precision=None)),
    Column("payment_status", String, nullable=True),
    Column("payment_method_id", String, nullable=False),
)

refunds = Table(
    "refunds",
    metadata,
    Column("payment_id", UUID, ForeignKey('content.payment.id', ondelete='CASCADE')),
    Column("refund_amount", UUID, ForeignKey('content.subscription.id', ondelete='CASCADE')),
    Column("payment_amount", DECIMAL(precision=None)),
    Column("refund_status", String, nullable=True),
    Column("external_refund_id", String, nullable=False),
)
