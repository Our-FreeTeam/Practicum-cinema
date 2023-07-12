from sqlalchemy import MetaData, Column, ForeignKey, TIMESTAMP, func, String, BOOLEAN, DECIMAL, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = MetaData()


class Subscription(Base):
    __tablename__ = "subscription"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    user_id = Column(UUID(as_uuid=True))
    start_date = Column(TIMESTAMP, default=func.now())
    end_date = Column(TIMESTAMP)
    subscription_type_id = Column(UUID(as_uuid=True), nullable=True)
    is_active = Column(BOOLEAN)
    is_repeatable = Column(BOOLEAN)


class SubscriptionType(Base):
    __tablename__ = "subscription_type"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String, nullable=False)
    amount = Column(DECIMAL(precision=None))
    is_active = Column(BOOLEAN)


class Payment(Base):
    __tablename__ = "payment"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("subscription.id", ondelete="CASCADE"))
    payment_amount = Column(DECIMAL(precision=None), nullable=False)
    payment_status = Column(String, nullable=True)
    payment_method_id = Column(String, nullable=False)
    payment_date = Column(TIMESTAMP, nullable=False)


class Refund(Base):
    __tablename__ = "refund"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    refund_amount = Column(DECIMAL(precision=None), nullable=False)
    refund_status = Column(String, nullable=True)
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("subscription.id", ondelete="CASCADE"))
    external_refund_id = Column(String, nullable=False)
    refund_date = Column(TIMESTAMP, nullable=False)


class SubscriptionHistory(Base):
    __tablename__ = "subscription_history"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    user_id = Column("user_id", UUID, ForeignKey("content.person.id", ondelete="CASCADE"))
    start_date = Column(TIMESTAMP, default=func.now())
    end_date = Column(TIMESTAMP)
    subscription_type_id = Column(UUID(as_uuid=True), nullable=True)
    is_active = Column(BOOLEAN)
    is_repeatable = Column(BOOLEAN)
    operation_date = Column(TIMESTAMP, nullable=False)
    operation_type = Column(String, nullable=False)


class SubscriptionTypeHistory(Base):
    __tablename__ = "subscription_type_history"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String, nullable=False)
    amount = Column(DECIMAL(precision=None))
    is_active = Column(BOOLEAN)
    operation_date = Column(TIMESTAMP, nullable=False)
    operation_type = Column(String, nullable=False)


class PaymentHistory(Base):
    __tablename__ = "payment_history"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("subscription.id", ondelete="CASCADE"))
    payment_amount = Column(DECIMAL(precision=None), nullable=False)
    payment_status = Column(String, nullable=True)
    payment_method_id = Column(String, nullable=False)
    payment_date = Column(TIMESTAMP, nullable=False)
    operation_date = Column(TIMESTAMP, nullable=False)
    operation_type = Column(String, nullable=False)


class RefundHistory(Base):
    __tablename__ = "refund_history"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    refund_amount = Column(DECIMAL(precision=None), ForeignKey("subscription.id", ondelete="CASCADE"))
    refund_status = Column(String, nullable=True)
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("subscription.id", ondelete="CASCADE"))
    external_refund_id = Column(String, nullable=False)
    refund_date = Column(TIMESTAMP, nullable=False)
    operation_date = Column(TIMESTAMP, nullable=False)
    operation_type = Column(String, nullable=False)
