sql_get_payment = """
    SELECT sub.user_id, p.payment_amount, p.payment_status, p.payment_date
    FROM payment p
    LEFT JOIN subscription sub on sub.id = p.subscription_id
    WHERE p.payment_status = 'succeeded'
    ORDER BY p.payment_date DESC;
"""

sql_get_refund = """
    SELECT sub.user_id, r.refund_amount, r.refund_status, r.refund_date
    FROM refund r
    LEFT JOIN subscription sub on sub.id = r.subscription_id
    WHERE r.refund_status = 'succeeded'
    ORDER BY r.refund_date DESC;
"""
