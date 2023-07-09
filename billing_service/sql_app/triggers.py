from alembic_utils.pg_trigger import PGTrigger

from sql_app.sql import update_subscription_history, update_payment_history, \
    update_subscription_type_history, \
    update_refund_history

subscription_history_trigger = PGTrigger(
    schema="public",
    signature="subscription_history_trigger",
    on_entity="public.subscription_history",
    definition=update_subscription_history
)
payment_history_trigger = PGTrigger(
    schema="public",
    signature="payment_history_trigger",
    on_entity="public.payment_history",
    definition=update_payment_history
)
subscription_type_history_trigger = PGTrigger(
    schema="public",
    signature="subscription_type_history_trigger",
    on_entity="public.subscription_type_history",
    definition=update_subscription_type_history
)
refund_history_trigger = PGTrigger(
    schema="public",
    signature="refund_history_trigger",
    on_entity="public.refund_history",
    definition=update_refund_history
)
