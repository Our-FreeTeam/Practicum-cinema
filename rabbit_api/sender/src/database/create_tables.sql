-- Создаем базовую таблицу для хранения отправленных уведомлений
CREATE TABLE IF NOT EXISTS notifications (
  notification_id uuid NOT NULL,
  user_id uuid NOT NULL,
  content_id varchar(250) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  type varchar(250) NOT NULL);
