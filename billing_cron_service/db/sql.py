sql = """
    SELECT sub.person_id, sub.subscription_type, sub_type.name, sub_type.amount
      FROM content.subscription sub
      LEFT JOIN content.subscription_type sub_type on sub.id = sub_type.subscription_id
     WHERE DATEDIFF(day, datetime.datetime.now(), sub.end_date) < 4 AND sub.is_active = 1
    ORDER BY sub.start_date;
"""

update_subscription_history = """
    CREATE OR REPLACE FUNCTION process_sub_history_audit_audit() RETURNS TRIGGER AS $subscription_history_trigger$
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
    $subscription_history$ LANGUAGE plpgsql;
    
    CREATE TRIGGER subscription_history_trigger
    AFTER INSERT OR UPDATE OR DELETE ON subscription_history
        FOR EACH ROW EXECUTE PROCEDURE process_sub_history_audit_audit();
"""

update_subscription_type_history = """
    CREATE OR REPLACE FUNCTION process_subscription_type_history_audit() RETURNS TRIGGER AS $subscription_type_history_trigger$
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
    $subscription_type_history$ LANGUAGE plpgsql;

    CREATE TRIGGER subscription_type_history_trigger
    AFTER INSERT OR UPDATE OR DELETE ON subscription_type_history
        FOR EACH ROW EXECUTE PROCEDURE process_subscription_type_history_audit();
"""

update_payment_history = """
    CREATE OR REPLACE FUNCTION process_payment_history_audit() RETURNS TRIGGER AS $payment_history_trigger$
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
    $payment_history$ LANGUAGE plpgsql;

    CREATE TRIGGER payment_history_trigger
    AFTER INSERT OR UPDATE OR DELETE ON payment_history
        FOR EACH ROW EXECUTE PROCEDURE process_payment_history_audit();
"""

update_refund_history = """
    CREATE OR REPLACE FUNCTION process_refund_history_audit() RETURNS TRIGGER AS $refund_history_trigger$
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
    $refund_history$ LANGUAGE plpgsql;

    CREATE TRIGGER refund_history_trigger
    AFTER INSERT OR UPDATE OR DELETE ON refund_history
        FOR EACH ROW EXECUTE PROCEDURE process_refund_history_audit();
"""
