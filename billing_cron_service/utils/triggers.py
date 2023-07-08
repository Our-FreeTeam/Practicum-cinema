from alembic_utils.pg_trigger import PGTrigger

from db.sql import update_subscription_history, update_payment_history, update_subscription_type_history, \
    update_refund_history

subscription_history_trigger = PGTrigger(
    schema="content",
    signature="subscription_history_trigger",
    on_entity="content.subscription_history",
    definition=update_subscription_history
)
payment_history_trigger = PGTrigger(
    schema="content",
    signature="payment_history_trigger",
    on_entity="content.payment_history",
    definition=update_payment_history
)
subscription_type_history_trigger = PGTrigger(
    schema="content",
    signature="subscription_type_history_trigger",
    on_entity="content.subscription_type_history",
    definition=update_subscription_type_history
)
refund_history_trigger = PGTrigger(
    schema="content",
    signature="refund_history_trigger",
    on_entity="content.refund_history",
    definition=update_refund_history
)
