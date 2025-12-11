# 🚀 Быстрый старт

## 📋 Содержание

- [Требования системы](#требования-системы)
- [Установка](#установка)
- [Запуск первого узла](#запуск-первого-узла)
- [Проверка работы](#проверка-работы)
- [Базовые примеры](#базовые-примеры)

---

## 🎯 Требования системы

### Системные требования

- **Python 3.8+** - основная среда выполнения
- **Операционная система**: Linux, macOS, Windows
- **RAM**: Не менее 1GB для базовой работы
- **Диск**: Не менее 1GB свободного места
- **Сеть**: Интернет подключение для работы с глобальной сетью

### Рекомендуемые конфигурации

#### Минимальная конфигурация
- CPU: 2 ядра
- RAM: 2GB
- Хранение: 10GB SSD
- Сеть: 10Mbps

#### Оптимальная конфигурация
- CPU: 4+ ядра
- RAM: 8GB+ 
- Хранение: 50GB+ SSD
- Сеть: 100Mbps+
- GPU: Опционально для ML задач

---

## 🛠️ Установка

### 1. Клонируем репозиторий

```bash
# Клонируем репозиторий
git clone https://github.com/p2pnet/p2pnet.git
cd p2pnet

# Или для SSH
git clone git@github.com:p2pnet/p2pnet.git
cd p2pnet
```

### 2. Создаем виртуальное окружение

```bash
# Для Linux/macOS
python -m venv venv
source venv/bin/activate

# Для Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Устанавливаем зависимости

```bash
# Устанавливаем основные зависимости
pip install -r requirements.txt

# Для разработки
pip install -r requirements-dev.txt

# Опционально: GPU поддержка
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 4. Проверяем установку

```bash
# Запуск тестов
python -m pytest tests/

# Проверка версии
python src/main.py --version
```

### 5. Конфигурация

```bash
# Копируем пример конфигурации
cp config/network_config.json.example config/network_config.json

# Редактируем конфигурацию под свои нужды
nano config/network_config.json
```

---

## 🚀 Запуск первого узла

### Базовый запуск

```bash
# Запуск узла по умолчанию
python src/main.py

# Запуск с указанными параметрами
python src/main.py --host 0.0.0.0 --port 5555 --debug

# Запуск с конфигурационным файлом
python src/main.py --config config/network_config.json
```

### Режимы запуска

#### 1. Стандартный режим
```bash
python src/main.py
```
- Автоматическое обнаружение сетей
- Подключение к известным bootstrap узлам
- Работа в локальной сети или через интернет

#### 2. Seed-режим (для серверов)
```bash
python src/main.py --seed --host 0.0.0.0 --port 5555
```
- Запуск как доверенного seed-узла
- Генерация root-ключей и сертификатов
- Создание подписанной конфигурации сети

#### 3. Глобальный режим
```bash
python src/main.py --global
```
- Поиск узлов по всему миру
- Подключение к глобальным DHT сетям
- Использование публичных реестров узлов

#### 4. Публичный режим
```bash
python src/main.py --public
```
- Работа как публичный узел с белым IP
- Принятие подключений от других узлов
- Регистрация в глобальных сетях

### Параметры командной строки

| Параметр | Описание | Пример |
|----------|----------|--------|
| `--host` | Адрес для прослушивания | `--host 0.0.0.0` |
| `--port` | Порт для прослушивания | `--port 5555` |
| `--bootstrap` | Bootstrap узлы | `--bootstrap d2omg.ru:5555` |
| `--seed` | Запуск в seed-режиме | `--seed` |
| `--public` | Запуск в публичном режиме | `--public` |
| `--global` | Глобальный режим поиска | `--global` |
| `--config` | Файл конфигурации | `--config config.json` |
| `--debug` | Режим отладки | `--debug` |

---

## ✅ Проверка работы

### 1. Проверка статуса

```bash
# Проверка статуса сети
python src/main.py --status

# Проверка здоровья
python src/main.py --health

# Экспорт данных
python src/main.py --export-data
```

### 2. Тестовое соединение

```bash
# Запуск тестового клиента
python examples/basic_usage.py

# Или интерактивный тест
python src/main.py --bootstrap d2omg.ru:5555
# В интерфейсе ввести: test
```

### 3. Мониторинг работы

```bash
# Просмотр логов
tail -f compute_network.log

# Мониторинг в реальном времени
python tools/monitor.py
```

---

## 💡 Базовые примеры

### Пример 1: Простые вычисления

```python
import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import ComputeNetwork
from core.task import Task, TaskType, TaskPriority

async def simple_computations():
    print("🧮 Простые вычисления")
    
    # Создаем сеть
    network = ComputeNetwork(host='127.0.0.1', port=5558)
    
    try:
        await network.start()
        await asyncio.sleep(2)
        
        # Задача: Сумма чисел от 1 до 1000
        sum_task = Task.create_range_reduce(
            owner_id=network.node.node_id,
            start=1,
            end=1000,
            operation="sum",
            requirements={'cpu_percent': 50.0, 'ram_gb': 1.0},
            privacy={
                "mode": "shard",
                "zk_verify": "basic"
            }
        )
        
        task_id = await network.submit_task(sum_task.to_dict())
        print(f"✅ Задача суммы создана: {task_id}")
        
        # Ждем завершения
        await asyncio.sleep(10)
        
        # Проверяем результат
        status = await network.get_task_status(task_id)
        print(f"📊 Результат: {status}")
        
    finally:
        await network.stop()

# Запуск
asyncio.run(simple_computations())
```

### Пример 2: Матричные операции

```python
import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import ComputeNetwork
from core.task import Task, TaskType, TaskPriority

async def matrix_example():
    print("🔢 Матричные операции")
    
    network = ComputeNetwork(host='127.0.0.1', port=5559)
    
    try:
        await network.start()
        await asyncio.sleep(2)
        
        # Создаем матрицы
        matrix1 = [[1, 2], [3, 4]]
        matrix2 = [[5, 6], [7, 8]]
        
        # Задача: Умножение матриц
        task = Task.create_matrix_ops(
            owner_id=network.node.node_id,
            matrix1=matrix1,
            matrix2=matrix2,
            operation="multiply",
            requirements={'cpu_percent': 50.0, 'ram_gb': 1.0}
        )
        
        task_id = await network.submit_task(task.to_dict())
        print(f"✅ Задача умножения создана: {task_id}")
        
        await asyncio.sleep(15)
        
        # Проверяем результат
        status = await network.get_task_status(task_id)
        print(f"📊 Результат умножения: {status}")
        
    finally:
        await network.stop()

# Запуск
asyncio.run(matrix_example())
```

### Пример 3: Machine Learning

```python
import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import ComputeNetwork
from core.task import Task, TaskType, TaskPriority

async def ml_example():
    print("🤖 Machine Learning пример")
    
    network = ComputeNetwork(host='127.0.0.1', port=5560)
    
    try:
        await network.start()
        await asyncio.sleep(2)
        
        # Генерируем тестовые данные
        train_data = [[[1, 2], [0]], [[3, 4], [1]], [[5, 6], [0]]]
        
        # Задача: Обучение модели
        train_task = Task.create_ml_train_step(
            owner_id=network.node.node_id,
            model_path="models/test_model.pkl",
            train_data=train_data,
            model_type="sklearn",
            requirements={'cpu_percent': 60.0, 'ram_gb': 2.0}
        )
        
        task_id = await network.submit_task(train_task.to_dict())
        print(f"✅ Задача обучения создана: {task_id}")
        
        await asyncio.sleep(20)
        
        # Проверяем результат
        status = await network.get_task_status(task_id)
        print(f"📊 Результат обучения: {status}")
        
    finally:
        await network.stop()

# Запуск
asyncio.run(ml_example())
```

### Пример 4: Пакетная обработка

```python
import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import ComputeNetwork
from core.task import Task, TaskType, TaskPriority

async def batch_processing_example():
    print("📦 Пакетная обработка данных")
    
    network = ComputeNetwork(host='127.0.0.1', port=5561)
    
    try:
        await network.start()
        await asyncio.sleep(2)
        
        # Создаем большой набор данных
        large_dataset = list(range(1, 10001))
        
        # Разбиваем на пакеты
        batch_size = 1000
        batches = [large_dataset[i:i + batch_size] for i in range(0, len(large_dataset), batch_size)]
        
        print(f"📦 Создано {len(batches)} пакетов по {batch_size} элементов")
        
        # Создаем задачи для каждого пакета
        task_ids = []
        for i, batch in enumerate(batches):
            task = Task.create_map_reduce(
                owner_id=network.node.node_id,
                data=batch,
                map_function="x ** 2",
                reduce_function="sum",
                requirements={'cpu_percent': 40.0, 'ram_gb': 1.0}
            )
            
            task_id = await network.submit_task(task.to_dict())
            task_ids.append(task_id)
            print(f"✅ Задача пакета {i+1} создана: {task_id}")
        
        # Ждем завершения всех задач
        await asyncio.sleep(30)
        
        # Собираем результаты
        total_sum = 0
        for task_id in task_ids:
            status = await network.get_task_status(task_id)
            if status['status'] == 'completed':
                result = status.get('result', {})
                total_sum += result.get('sum', 0)
                print(f"✅ Пакет завершен, сумма: {result.get('sum', 0)}")
        
        print(f"🎉 Обработка завершена, итоговая сумма: {total_sum}")
        
    finally:
        await network.stop()

# Запуск
asyncio.run(batch_processing_example())
```

---

## 🎯 Следующие шаги

После успешного запуска первого узла:

1. **Добавьте больше узлов** в сеть
2. **Настройте конфигурацию** под ваши нужды
3. **Изучите API** для интеграции с другими системами
4. **Попробуйте продвинутые примеры** из раздела examples/
5. **Настройте мониторинг** и логирование

> 💡 **Совет**: Для начала запустите несколько узлов на одной машине с разными портами, чтобы понять принцип работы сети.

---

## 📚 Дополнительные ресурсы

- [Полное руководство](../comprehensive-guide.md) - подробное описание всех возможностей
- [API документация](../api-reference.md) - техническая документация API
- [Примеры использования](../examples.md) - готовые примеры кода
- [Руководство по развертыванию](../deployment.md) - продвинутые сценарии部署
- [FAQ](../faq.md) - ответы на частые вопросы

🚀 **Готовы начать? Запустите свой первый узел прямо сейчас!**
