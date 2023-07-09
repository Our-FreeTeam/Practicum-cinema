from alembic_utils.pg_trigger import PGTrigger

from sql_app.sql import subscription_history_trigger, payment_history_trigger, subscription_type_history_trigger, \
    refund_history_trigger

trigger_subscription_history = PGTrigger(
    schema="public",
    signature="trigger_subscription_history",
    on_entity="public.subscription_history",
    definition=subscription_history_trigger
)
trigger_payment_history = PGTrigger(
    schema="public",
    signature="trigger_payment_history",
    on_entity="public.payment_history",
    definition=payment_history_trigger
)
trigger_subscription_type_history = PGTrigger(
    schema="public",
    signature="trigger_subscription_type_history",
    on_entity="public.subscription_type_history",
    definition=subscription_type_history_trigger
)
trigger_refund_history = PGTrigger(
    schema="public",
    signature="trigger_refund_history",
    on_entity="public.refund_history",
    definition=refund_history_trigger
)
