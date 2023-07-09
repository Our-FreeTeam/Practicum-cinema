sql_get_payment = """
    SELECT user_id, payment_amount, payment_status, payment_date
      FROM payment
     WHERE payment_status == 'succeeded'
    ORDER BY payment_date DESC;
"""

sql_get_refund = """
    SELECT user_id, refund_amount, refund_status, refund_date
      FROM refund
     WHERE refund_status == 'succeeded'
    ORDER BY refund_date DESC;
"""
