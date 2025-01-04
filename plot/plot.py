import pandas as pd
import matplotlib.pyplot as plt
import time
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Путь к файлу с метриками
METRIC_LOG_PATH = './logs/metric_log.csv'

def read_first_5_lines():
    """
    Читает и логирует первые 5 строк из файла metric_log.csv.
    """
    try:
        df = pd.read_csv(METRIC_LOG_PATH)
        logging.debug("PLOT: Первые 5 строк из metric_log.csv:")
        logging.debug(df.head())  # Логируем первые 5 строк
    except Exception as e:
        logging.error(f"Ошибка при чтении metric_log.csv: {e}")

# Основной цикл для построения и обновления графика
while True:
    try:
        logging.debug("Чтение данных из metric_log.csv")
        # Загрузка данных из CSV
        df = pd.read_csv(METRIC_LOG_PATH)

        # Логируем первые 5 строк
        read_first_5_lines()

        # Создание гистограммы
        plt.figure(figsize=(10, 6))
        plt.hist(
            df['absolute_error'],  # Данные для гистограммы
            bins=30,               # Количество интервалов
            color='skyblue',       # Цвет столбцов
            edgecolor='black'      # Цвет границ
        )
        plt.title('Распределение абсолютных ошибок')
        plt.xlabel('Абсолютная ошибка')
        plt.ylabel('Частота')

        # Сохранение графика
        plt.savefig('./logs/error_distribution.png')
        logging.debug("График сохранён в logs/error_distribution.png")
        plt.close()

        # Задержка перед следующим обновлением
        time.sleep(10)

    except Exception as e:
        logging.error(f"Ошибка при построении графика: {e}")
        time.sleep(5)  # Повторная попытка через 5 секунд