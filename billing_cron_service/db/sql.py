sql = """
    SELECT sub.person_id, sub.subscription_type, sub_types.name, sub_types.amount
      FROM content.subscriptions sub
      LEFT JOIN content.subscription_types sub_types on sub.id = sub_types.subscription_id
     WHERE DATEDIFF(day, datetime.datetime.now(), sub.end_date) < 4 AND sub.is_active = 1
    ORDER BY sub.start_date;
"""

update_subscriptions_history = """
    CREATE OR REPLACE FUNCTION process_sub_history_audit_audit() RETURNS TRIGGER AS $subscriptions_history_trigger$
        BEGIN
            --
            -- Create a row in subscriptions_history to reflect the operation performed on emp,
            -- make use of the special variable TG_OP to work out the operation.
            -- TG_OP - Data type text; a string of INSERT, UPDATE, DELETE, or TRUNCATE telling 
            -- for which operation the trigger was fired.
            IF (TG_OP = 'DELETE') THEN
                INSERT INTO subscriptions_history SELECT OLD.*, now(), 'D';
                RETURN OLD;
            ELSIF (TG_OP = 'UPDATE') THEN
                INSERT INTO subscriptions_history SELECT NEW.*, now(), 'U';
                RETURN NEW;
            ELSIF (TG_OP = 'INSERT') THEN
                INSERT INTO subscriptions_history SELECT NEW.*, now(), 'I';
                RETURN NEW;
            END IF;
            RETURN NULL; -- result is ignored since this is an AFTER trigger
        END;
    $subscriptions_history$ LANGUAGE plpgsql;
    
    CREATE TRIGGER subscriptions_history_trigger
    AFTER INSERT OR UPDATE OR DELETE ON subscriptions_history
        FOR EACH ROW EXECUTE PROCEDURE process_sub_history_audit_audit();
"""

update_subscription_types_history = """
    CREATE OR REPLACE FUNCTION process_subscription_types_history_audit() RETURNS TRIGGER AS $subscription_types_history_trigger$
        BEGIN
            --
            -- Create a row in subscriptions_history to reflect the operation performed on emp,
            -- make use of the special variable TG_OP to work out the operation.
            -- TG_OP - Data type text; a string of INSERT, UPDATE, DELETE, or TRUNCATE telling 
            -- for which operation the trigger was fired.
            IF (TG_OP = 'DELETE') THEN
                INSERT INTO subscription_types_history SELECT OLD.*, now(), 'D';
                RETURN OLD;
            ELSIF (TG_OP = 'UPDATE') THEN
                INSERT INTO subscription_types_history SELECT NEW.*, now(), 'U';
                RETURN NEW;
            ELSIF (TG_OP = 'INSERT') THEN
                INSERT INTO subscription_types_history SELECT NEW.*, now(), 'I';
                RETURN NEW;
            END IF;
            RETURN NULL; -- result is ignored since this is an AFTER trigger
        END;
    $subscription_types_history$ LANGUAGE plpgsql;

    CREATE TRIGGER subscription_types_history_trigger
    AFTER INSERT OR UPDATE OR DELETE ON subscription_types_history
        FOR EACH ROW EXECUTE PROCEDURE process_subscription_types_history_audit();
"""

update_payments_history = """
    CREATE OR REPLACE FUNCTION process_payments_history_audit() RETURNS TRIGGER AS $payments_history_trigger$
        BEGIN
            --
            -- Create a row in subscriptions_history to reflect the operation performed on emp,
            -- make use of the special variable TG_OP to work out the operation.
            -- TG_OP - Data type text; a string of INSERT, UPDATE, DELETE, or TRUNCATE telling 
            -- for which operation the trigger was fired.
            IF (TG_OP = 'DELETE') THEN
                INSERT INTO payments_history SELECT OLD.*, now(), 'D';
                RETURN OLD;
            ELSIF (TG_OP = 'UPDATE') THEN
                INSERT INTO payments_history SELECT NEW.*, now(), 'U';
                RETURN NEW;
            ELSIF (TG_OP = 'INSERT') THEN
                INSERT INTO payments_history SELECT NEW.*, now(), 'I';
                RETURN NEW;
            END IF;
            RETURN NULL; -- result is ignored since this is an AFTER trigger
        END;
    $payments_history$ LANGUAGE plpgsql;

    CREATE TRIGGER payments_history_trigger
    AFTER INSERT OR UPDATE OR DELETE ON payments_history
        FOR EACH ROW EXECUTE PROCEDURE process_payments_history_audit();
"""

update_refunds_history = """
    CREATE OR REPLACE FUNCTION process_refunds_history_audit() RETURNS TRIGGER AS $refunds_history_trigger$
        BEGIN
            --
            -- Create a row in subscriptions_history to reflect the operation performed on emp,
            -- make use of the special variable TG_OP to work out the operation.
            -- TG_OP - Data type text; a string of INSERT, UPDATE, DELETE, or TRUNCATE telling 
            -- for which operation the trigger was fired.
            IF (TG_OP = 'DELETE') THEN
                INSERT INTO refunds_history SELECT OLD.*, now(), 'D';
                RETURN OLD;
            ELSIF (TG_OP = 'UPDATE') THEN
                INSERT INTO refunds_history SELECT NEW.*, now(), 'U';
                RETURN NEW;
            ELSIF (TG_OP = 'INSERT') THEN
                INSERT INTO refunds_history SELECT NEW.*, now(), 'I';
                RETURN NEW;
            END IF;
            RETURN NULL; -- result is ignored since this is an AFTER trigger
        END;
    $refunds_history$ LANGUAGE plpgsql;

    CREATE TRIGGER refunds_history_trigger
    AFTER INSERT OR UPDATE OR DELETE ON refunds_history
        FOR EACH ROW EXECUTE PROCEDURE process_refunds_history_audit();
"""
