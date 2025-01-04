#!/bin/bash
set -e  # Завершить скрипт при любой ошибке

# Хост RabbitMQ
host="rabbitmq"
shift  # Сдвигаем аргументы, чтобы оставить только команду для выполнения

# Ожидание доступности RabbitMQ
until nc -z "$host" 5672; do
  >&2 echo "RabbitMQ недоступен — ждём..."
  sleep 1
done

# Когда RabbitMQ станет доступен
>&2 echo "RabbitMQ доступен — выполняем команду"
exec "$@"  # Запуск переданной команды