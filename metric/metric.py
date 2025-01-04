import pika
import json
import time
import logging
import pandas as pd
import numpy as np
import os

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Путь к файлу лога
METRIC_LOG_PATH = './logs/metric_log.csv'

# Словари для хранения значений y_true и y_pred
y_true_dict = {}
y_pred_dict = {}

# Проверка существования файла и его создание, если нужно
if not os.path.exists(METRIC_LOG_PATH):
    logging.debug(f"Файл {METRIC_LOG_PATH} не существует, создаём новый.")

def write_to_csv(message_id, y_true_value, y_pred_value, absolute_error):
    """
    Записывает данные в CSV-файл.
    """
    try:
        # Создаём DataFrame для записи
        df = pd.DataFrame({
            'id': [message_id],
            'y_true': [y_true_value],
            'y_pred': [y_pred_value],
            'absolute_error': [absolute_error]
        })

        # Логируем данные перед записью
        logging.debug(f"Записываем в CSV: {df}")

        # Проверяем, существует ли файл
        file_exists = os.path.exists(METRIC_LOG_PATH)

        # Записываем данные в файл
        df.to_csv(METRIC_LOG_PATH, mode='a', header=not file_exists, index=False)
        logging.debug(f"Данные для id {message_id} записаны в {METRIC_LOG_PATH}")

    except Exception as e:
        logging.error(f"Ошибка при записи в CSV: {e}")

def read_first_5_lines():
    """
    Читает и логирует первые 5 строк из CSV-файла.
    """
    try:
        df = pd.read_csv(METRIC_LOG_PATH)
        logging.debug("Первые 5 строк из metric_log.csv:")
        logging.debug(df.head())
    except Exception as e:
        logging.error(f"Ошибка при чтении metric_log.csv: {e}")

def callback(ch, method, properties, body):
    """
    Функция обработки сообщений из RabbitMQ.
    """
    logging.debug(f"Получено сообщение из очереди {method.routing_key}: {body}")
    try:
        message = json.loads(body)
        message_id = message['id']

        # Сохраняем значения в соответствующие словари
        if method.routing_key == 'y_true':
            y_true_dict[message_id] = message['body']
            logging.debug(f"Сохранено y_true для id {message_id}")
        elif method.routing_key == 'y_pred':
            y_pred_dict[message_id] = message['body']
            logging.debug(f"Сохранено y_pred для id {message_id}")

        # Если есть оба значения, вычисляем абсолютную ошибку
        if message_id in y_true_dict and message_id in y_pred_dict:
            y_true_value = y_true_dict[message_id]
            y_pred_value = y_pred_dict[message_id]
            absolute_error = abs(y_true_value - y_pred_value)
            logging.debug(f"Абсолютная ошибка для id {message_id}: {absolute_error}")

            # Записываем данные в CSV
            write_to_csv(message_id, y_true_value, y_pred_value, absolute_error)

        # Логируем первые 5 строк из CSV
        read_first_5_lines()

    except Exception as e:
        logging.error(f"Ошибка при обработке сообщения: {e}")

# Основной цикл для подключения к RabbitMQ
while True:
    try:
        # Подключение к RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()

        # Объявляем очереди
        channel.queue_declare(queue='y_true', durable=True)
        channel.queue_declare(queue='y_pred', durable=True)
        logging.debug("Очереди y_true и y_pred объявлены")

        # Настройка потребителей
        channel.basic_consume(queue='y_true', on_message_callback=callback, auto_ack=True)
        channel.basic_consume(queue='y_pred', on_message_callback=callback, auto_ack=True)

        logging.debug('Ожидание сообщений. Для выхода нажмите CTRL+C')
        channel.start_consuming()
        break

    except Exception as e:
        logging.error(f"Ошибка при подключении к RabbitMQ: {e}")
        time.sleep(5)