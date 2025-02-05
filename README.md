## Этап 1: Отправка данных с уникальными идентификаторами в RabbitMQ

На первом этапе реализуем отправку данных в очереди RabbitMQ. Для этого:

1. В цикле добавлена задержка с помощью `time.sleep(10)`.
2. Генерация уникальных идентификаторов (`message_id`) с использованием временной метки (`datetime.timestamp()`).
3. Отправка двух сообщений:
   - В очередь `y_true` с истинными значениями.
   - В очередь `features` с признаками.
   Оба сообщения содержат одинаковый `message_id`.

Код в `features.py`:

- Для каждого сообщения создаётся уникальный идентификатор.
- После каждой итерации добавляется задержка.

---

## Этап 2: Логирование метрик в файл `metric_log.csv`

На втором этапе реализуем сервис для логирования метрик. Он будет:

1. Подписываться на очереди `y_true` и `features`.
2. Сохранять полученные значения в словарях по уникальным идентификаторам.
3. При получении данных для одного `message_id` вычислять абсолютную ошибку и записывать её в файл `metric_log.csv`.

Код в `metric.py`:

- Подписка на очереди.
- Хранение данных в словарях.
- Запись результатов в CSV-файл.

---

## Этап 3: Построение гистограммы абсолютных ошибок

На третьем этапе реализуем сервис для визуализации данных. Он будет:

1. Читать данные из `metric_log.csv` каждые 10 секунд.
2. Строить гистограмму абсолютных ошибок с использованием `matplotlib`.
3. Сохранять график в файл `error_distribution.png` в папке `logs/`.

Код в `plot.py`:

- Чтение данных из CSV.
- Построение и обновление гистограммы.
- Сохранение графика.

---

## Этап 4: Настройка Docker и docker-compose

Для удобства развёртывания созданы Dockerfile для каждого сервиса.

---

## Этап 5: Запуск приложения

Сборка и запуск контейнеров:

```bash
docker-compose build --no-cache
docker-compose up
```

После запуска сервисы начнут работать в режиме реального времени, обновляя графики с каждой новой итерацией.

---