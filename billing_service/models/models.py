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
