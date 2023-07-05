sql = """
    SELECT sub.user_id, sub.subscription_type, sub_types.name, sub_types.amount
      FROM content.subscriptions sub
      LEFT JOIN content.subscription_types sub_types on sub.id = sub_types.subscription_id
     WHERE DATEDIFF(day, datetime.datetime.now(), sub.end_date) < 4 AND sub.is_active = 1
    ORDER BY sub.start_date;
"""