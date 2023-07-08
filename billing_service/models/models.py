from sqlalchemy import MetaData, Column, ForeignKey, TIMESTAMP, func, String, BOOLEAN, DECIMAL, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = MetaData()


class Subscriptions(Base):
    __tablename__ = "subscriptions"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('uuid_generate_v4()'))
    user_id = Column(UUID(as_uuid=True))
    start_date = Column(TIMESTAMP, default=func.now())
    end_date = Column(TIMESTAMP)
    subscription_type_id = Column(UUID(as_uuid=True), nullable=True)
    is_active = Column(BOOLEAN)
    is_repeatable = Column(BOOLEAN)


class SubscriptionTypes(Base):
    __tablename__ = "subscription_types"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('uuid_generate_v4()'))
    name = Column(String, nullable=False)
    subscriptions_id = Column(UUID(as_uuid=True), ForeignKey('subscriptions.id', ondelete='CASCADE'))
    refund_amount = Column(DECIMAL(precision=None))
    is_active = Column(BOOLEAN)


class Payments(Base):
    __tablename__ = "payments"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('uuid_generate_v4()'))
    subscriptions_id = Column(UUID(as_uuid=True), ForeignKey('subscriptions.id', ondelete='CASCADE'))
    payment_amount = Column(DECIMAL(precision=None))
    payment_status = Column(String, nullable=True)
    payment_method_id = Column(String, nullable=False)
    payment_date = Column(TIMESTAMP, nullable=False)


class Refunds(Base):
    __tablename__ = "refunds"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('uuid_generate_v4()'))
    payments_id = Column(UUID(as_uuid=True), ForeignKey('payments.id', ondelete='CASCADE'))
    refund_amount = Column(DECIMAL(precision=None), ForeignKey('subscriptions.id', ondelete='CASCADE'))
    payment_amount = Column(DECIMAL(precision=None))
    refund_status = Column(String, nullable=True)
    external_refund_id = Column(String, nullable=False)
    refund_date = Column(TIMESTAMP, nullable=False)

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
