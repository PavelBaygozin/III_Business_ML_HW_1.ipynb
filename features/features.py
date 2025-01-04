import pika
import numpy as np
import json
from sklearn.datasets import load_diabetes
import time
from datetime import datetime
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def send_messages():
    """
    Основная функция для отправки сообщений в RabbitMQ.
    """
    while True:
        try:
            # Загрузка датасета о диабете
            logging.debug("Загрузка датасета о диабете")
            X, y = load_diabetes(return_X_y=True)
            logging.debug(f"Загружен датасет X: {X.shape} строк, y: {y.shape} значений")

            # Выбор случайной строки из датасета
            random_row = np.random.randint(0, X.shape[0] - 1)
            logging.debug(f"Выбрана случайная строка: {random_row}")
            logging.debug(f"Значение y для выбранной строки: {y[random_row]}")

            # Генерация уникального идентификатора сообщения
            message_id = datetime.timestamp(datetime.now())
            logging.debug(f"Сгенерирован уникальный идентификатор сообщения: {message_id}")

            # Подключение к RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel()

            # Объявление очередей
            channel.queue_declare(queue='y_true', durable=True)
            channel.queue_declare(queue='features', durable=True)
            logging.debug("Очереди y_true и features объявлены")

            # Формирование и отправка сообщения в очередь y_true
            message_y_true = {
                'id': message_id,
                'body': float(y[random_row])  # Преобразуем в float для совместимости
            }
            channel.basic_publish(
                exchange='',
                routing_key='y_true',
                body=json.dumps(message_y_true)
            )
            logging.debug(f"Сообщение отправлено в очередь y_true (ID: {message_id})")

            # Формирование и отправка сообщения в очередь features
            message_features = {
                'id': message_id,
                'body': X[random_row].tolist()  # Преобразуем в список для JSON
            }
            channel.basic_publish(
                exchange='',
                routing_key='features',
                body=json.dumps(message_features)
            )
            logging.debug(f"Сообщение отправлено в очередь features (ID: {message_id})")

            # Закрытие подключения
            connection.close()
            logging.debug(f"Подключение к RabbitMQ закрыто для сообщения с ID: {message_id}")

            # Задержка перед следующей итерацией
            time.sleep(10)

        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения: {e}")
            time.sleep(5)  # Повторная попытка через 5 секунд

# Запуск функции отправки сообщений
if __name__ == "__main__":
    send_messages()