# Используем базовый образ Python 3.9
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем netcat для проверки доступности RabbitMQ
RUN apt-get update && apt-get install -y netcat-openbsd

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта
COPY . .

# Копируем скрипт для ожидания RabbitMQ и делаем его исполняемым
COPY features/wait-for-rabbitmq.sh .
RUN chmod +x wait-for-rabbitmq.sh

# Запуск скрипта ожидания и основного приложения
CMD ["./wait-for-rabbitmq.sh", "rabbitmq:5672", "--", "python", "plot/plot.py"]