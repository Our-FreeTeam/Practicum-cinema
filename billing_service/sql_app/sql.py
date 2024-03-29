sql = """
    SELECT sub.user_id, sub_type.name as subscription_name, sub_type.amount
    FROM subscription sub
    LEFT JOIN subscription_type sub_type on sub.subscription_type_id = sub_type.id
    WHERE date_part('day', CURRENT_DATE - sub.end_date) < 4 AND sub.is_active = TRUE
    ORDER BY sub.start_date;
"""

sql_auto_sub = """
    SELECT sub.user_id, p.payment_method_id, sub_type.name as subscription_name, sub_type.amount
    FROM subscription sub
    LEFT JOIN subscription_type sub_type on sub.subscription_type_id = sub_type.id
    LEFT JOIN payment p on sub.id = p.subscription_id
    WHERE date_part('day', CURRENT_DATE - sub.end_date) < 4 AND sub.is_active = TRUE
    ORDER BY sub.start_date;
"""

subscription_history_func = """
    CREATE OR REPLACE FUNCTION process_subscription_history_audit()
    RETURNS TRIGGER AS $subscription_history_trigger$
        BEGIN
            --
            -- Create a row in subscription_history to reflect the operation performed on emp,
            -- make use of the special variable TG_OP to work out the operation.
            -- TG_OP - Data type text; a string of INSERT, UPDATE, DELETE, or TRUNCATE telling
            -- for which operation the trigger was fired.
            IF (TG_OP = 'DELETE') THEN
                INSERT INTO subscription_history SELECT OLD.*, now(), 'D';
                RETURN OLD;
            ELSIF (TG_OP = 'UPDATE') THEN
                INSERT INTO subscription_history SELECT NEW.*, now(), 'U';
                RETURN NEW;
            ELSIF (TG_OP = 'INSERT') THEN
                INSERT INTO subscription_history SELECT NEW.*, now(), 'I';
                RETURN NEW;
            END IF;
            RETURN NULL; -- result is ignored since this is an AFTER trigger
        END;
    $subscription_history_trigger$ LANGUAGE plpgsql;
"""

subscription_type_history_func = """
    CREATE OR REPLACE FUNCTION process_subscription_type_history_audit()
    RETURNS TRIGGER AS $subscription_type_history_trigger$
        BEGIN
            --
            -- Create a row in subscription_type to reflect the operation performed on emp,
            -- make use of the special variable TG_OP to work out the operation.
            -- TG_OP - Data type text; a string of INSERT, UPDATE, DELETE, or TRUNCATE telling
            -- for which operation the trigger was fired.
            IF (TG_OP = 'DELETE') THEN
                INSERT INTO subscription_type_history SELECT OLD.*, now(), 'D';
                RETURN OLD;
            ELSIF (TG_OP = 'UPDATE') THEN
                INSERT INTO subscription_type_history SELECT NEW.*, now(), 'U';
                RETURN NEW;
            ELSIF (TG_OP = 'INSERT') THEN
                INSERT INTO subscription_type_history SELECT NEW.*, now(), 'I';
                RETURN NEW;
            END IF;
            RETURN NULL; -- result is ignored since this is an AFTER trigger
        END;
    $subscription_type_history_trigger$ LANGUAGE plpgsql;
"""

payment_history_func = """
    CREATE OR REPLACE FUNCTION process_payment_history_audit()
    RETURNS TRIGGER AS $payment_history_trigger$
        BEGIN
            --
            -- Create a row in payment_history to reflect the operation performed on emp,
            -- make use of the special variable TG_OP to work out the operation.
            -- TG_OP - Data type text; a string of INSERT, UPDATE, DELETE, or TRUNCATE telling
            -- for which operation the trigger was fired.
            IF (TG_OP = 'DELETE') THEN
                INSERT INTO payment_history SELECT OLD.*, now(), 'D';
                RETURN OLD;
            ELSIF (TG_OP = 'UPDATE') THEN
                INSERT INTO payment_history SELECT NEW.*, now(), 'U';
                RETURN NEW;
            ELSIF (TG_OP = 'INSERT') THEN
                INSERT INTO payment_history SELECT NEW.*, now(), 'I';
                RETURN NEW;
            END IF;
            RETURN NULL; -- result is ignored since this is an AFTER trigger
        END;
    $payment_history_trigger$ LANGUAGE plpgsql;
"""

refund_history_func = """
    CREATE OR REPLACE FUNCTION process_refund_history_audit()
    RETURNS TRIGGER AS $refund_history_trigger$
        BEGIN
            --
            -- Create a row in refund_history to reflect the operation performed on emp,
            -- make use of the special variable TG_OP to work out the operation.
            -- TG_OP - Data type text; a string of INSERT, UPDATE, DELETE, or TRUNCATE telling
            -- for which operation the trigger was fired.
            IF (TG_OP = 'DELETE') THEN
                INSERT INTO refund_history SELECT OLD.*, now(), 'D';
                RETURN OLD;
            ELSIF (TG_OP = 'UPDATE') THEN
                INSERT INTO refund_history SELECT NEW.*, now(), 'U';
                RETURN NEW;
            ELSIF (TG_OP = 'INSERT') THEN
                INSERT INTO refund_history SELECT NEW.*, now(), 'I';
                RETURN NEW;
            END IF;
            RETURN NULL; -- result is ignored since this is an AFTER trigger
        END;
    $refund_history_trigger$ LANGUAGE plpgsql;
"""

subscription_history_trigger = """
    CREATE TRIGGER subscription_history_trigger
    AFTER INSERT OR UPDATE OR DELETE ON subscription_history
        FOR EACH ROW EXECUTE PROCEDURE process_subscription_history_audit();
"""

subscription_type_history_trigger = """
    CREATE TRIGGER subscription_type_history_trigger
    AFTER INSERT OR UPDATE OR DELETE ON subscription_type_history
        FOR EACH ROW EXECUTE PROCEDURE process_subscription_type_history_audit();
"""

payment_history_trigger = """
    CREATE TRIGGER payment_history_trigger
    AFTER INSERT OR UPDATE OR DELETE ON payment_history
        FOR EACH ROW EXECUTE PROCEDURE process_payment_history_audit();
"""

refund_history_trigger = """
    CREATE TRIGGER refund_history_trigger
    AFTER INSERT OR UPDATE OR DELETE ON refund_history
        FOR EACH ROW EXECUTE PROCEDURE process_refund_history_audit();
"""

# Удаление таблиц и триггеров
drop_subscription_history_func = """
    DROP FUNCTION IF EXISTS process_subscription_history_audit();
"""

drop_payment_history_func = """
    DROP FUNCTION IF EXISTS process_subscription_type_history_audit();
"""

drop_subscription_type_history_func = """
    DROP FUNCTION IF EXISTS process_payment_history_audit();
"""

drop_refund_history_func = """
    DROP FUNCTION IF EXISTS process_refund_history_audit();
"""

drop_subscription_history_trigger = """
    DROP TRIGGER IF EXISTS subscription_history_trigger;
"""

drop_payment_history_trigger = """
    DROP TRIGGER IF EXISTS subscription_type_history_trigger;
"""

drop_subscription_type_history_trigger = """
    DROP TRIGGER IF EXISTS payment_history_trigger;
"""

drop_refund_history_trigger = """
    DROP TRIGGER IF EXISTS refund_history_trigger;
"""
