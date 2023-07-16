insert_payment = """
insert into payment (id, subscription_id, payment_amount, payment_status, payment_method_id, payment_date)
values  ('70328b9b-88f9-4126-851f-96bfc8e6e1e6', '96876723-ea9f-4c0a-a087-8e5a269d232c', 1000, 'succeeded', '6c3ec743-1bea-4733-b9c9-21c749517434', '2023-07-14 18:20:17.95'),
        ('0b0ba13d-7773-4c16-8010-985a23779c01', 'f834225f-3e1a-4332-8851-12e1de0966ea', 1000, 'succeeded', '6c3ec743-1bea-4733-b9c9-21c749517434', '2023-08-14 18:20:17.95');
    """
