sql = """
    SELECT sub.user_id, sub_type.name as subscription_name, sub_type.amount
    FROM subscription sub
    LEFT JOIN subscription_type sub_type on sub.subscription_type_id = sub_type.id
    WHERE date_part('day', CURRENT_DATE - sub.end_date) < 4 AND sub.is_active = TRUE AND sub.is_repeatable = TRUE
    ORDER BY sub.start_date;
"""

sql_auto_sub = """
    SELECT sub.user_id, p.payment_method_id, sub_type.name as subscription_name, sub_type.amount
    FROM subscription sub
    LEFT JOIN subscription_type sub_type on sub.subscription_type_id = sub_type.id
    LEFT JOIN payment p on sub.id = p.subscription_id
    WHERE date_part('day', CURRENT_DATE - sub.end_date) < 4 AND sub.is_active = TRUE AND sub.is_repeatable = TRUE
    ORDER BY sub.start_date;
"""