#!/usr/bin/env bash


set -e

# переносим значения переменных из текущего окружения
env | while read -r LINE; do  # читаем результат команды 'env' построчно
    # делим строку на две части, используя в качестве разделителя "=" (см. IFS)
    IFS="=" read VAR VAL <<< ${LINE}
    # удаляем все предыдущие упоминания о переменной, игнорируя код возврата
    sed --in-place "/^${VAR}/d" /etc/security/pam_env.conf || true
    # добавляем определение новой переменной в конец файла
    echo "${VAR} DEFAULT=\"${VAL}\"" >> /etc/security/pam_env.conf
done

exec "$@"

# This script checks if the container is started for the first time.

CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"
if [ ! -e /$CONTAINER_FIRST_STARTUP ]; then
    touch /$CONTAINER_FIRST_STARTUP
    # first startup.
    rm -rf /opt/app/requirements.txt
    touch /var/log/cron.log
    locale -a
fi

#cron -f
busybox syslogd -C; cron -L 2 -f