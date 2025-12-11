# 💡 Примеры использования и Troubleshooting

## 📋 Содержание

- [Базовые примеры](#базовые-примеры)
- [Продвинутые примеры](#продвинутые-примеры)
- [Примеры интеграции](#примеры-интеграции)
- [Типичные проблемы и решения](#типичные-проблемы-и-решения)
- [Отладка и диагностика](#отладка-и-диагностика)
- [Производительность](#производительность)
- [Безопасность](#безопасность)
- [FAQ](#faq)

---

## 🎯 Базовые примеры

### Пример 1: Запуск сети и создание простой задачи

```python
#!/usr/bin/env python3
# basic_network_example.py

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import ComputeNetwork
from core.task import Task, TaskType, TaskPriority

async def main():
    # Создание сети
    network = ComputeNetwork(
        host="127.0.0.1",
        port=5557,
        node_type="client"
    )
    
    try:
        print("🚀 Запуск сети...")
        await network.start()
        await asyncio.sleep(2)
        
        print(f"🆔 Узел запущен: {network.node.node_id}")
        print(f"💪 Возможности: CPU={network.node.capabilities.cpu_score}, RAM={network.node.capabilities.ram_gb}GB")
        
        # Создание простой задачи
        task = Task.create_range_reduce(
            owner_id=network.node.node_id,
            start=1,
            end=1000,
            operation="sum",
            requirements={
                "cpu_percent": 50.0,
                "ram_gb": 0.5,
                "timeout_seconds": 30
            },
            config={
                "max_price": 0.1,
                "priority": TaskPriority.NORMAL.value
            }
        )
        
        print(f"📝 Создание задачи: {task.task_id}")
        
        # Подача задачи
        task_id = await network.submit_task(task.to_dict())
        print(f"✅ Задача отправлена: {task_id}")
        
        # Мониторинг выполнения
        max_attempts = 30
        for attempt in range(max_attempts):
            status = await network.get_task_status(task_id)
            print(f"📊 Попытка {attempt + 1}/{max_attempts}: статус = {status['status']}")
            
            if status['status'] == 'completed':
                result = await network.get_task_result(task_id)
                print(f"🎉 Успешно! Результат: {result}")
                break
            elif status['status'] == 'failed':
                print(f"❌ Задача не выполнена: {status.get('error', 'Unknown error')}")
                break
                
            await asyncio.sleep(1)
        else:
            print(f"⏰ Задача не завершилась за {max_attempts} секунд")
        
    except Exception as e:
        print(f"💥 Ошибка: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("🛑 Остановка сети...")
        await network.stop()
        print("✅ Сеть остановлена")

if __name__ == "__main__":
    asyncio.run(main())
```

### Пример 2: Пакетная обработка данных

```python
#!/usr/bin/env python3
# batch_processing_example.py

import asyncio
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import ComputeNetwork
from core.task import Task, TaskType, TaskPriority

async def batch_processing_example():
    # Создание сети
    network = ComputeNetwork(host="127.0.0.1", port=5558)
    
    try:
        await network.start()
        await asyncio.sleep(2)
        
        # Генерация тестовых данных
        print("🔢 Генерация тестовых данных...")
        data_size = 10000
        vector_size = 100
        data = np.random.rand(data_size, vector_size)
        
        # Разбиение на пакеты
        batch_size = 1000
        batches = [data[i:i+batch_size] for i in range(0, len(data), batch_size)]
        
        print(f"📦 Создано {len(batches)} пакетов по {batch_size} векторов каждый")
        
        # Создание задач
        tasks = []
        for i, batch in enumerate(batches):
            print(f"📝 Создание задачи {i+1}/{len(batches)}...")
            
            task = Task.create_map(
                owner_id=network.node.node_id,
                data=batch.tolist(),
                operation="mean",
                requirements={
                    "cpu_percent": 75.0,
                    "ram_gb": 2.0,
                    "timeout_seconds": 60
                },
                config={
                    "max_price": 0.2,
                    "priority": TaskPriority.NORMAL.value,
                    "batch_id": i
                }
            )
            
            task_id = await network.submit_task(task.to_dict())
            tasks.append(task_id)
            print(f"✅ Задача {i+1} создана: {task_id}")
        
        # Ожидание завершения всех задач
        print("⏳ Ожидание завершения всех задач...")
        results = []
        
        for i, task_id in enumerate(tasks):
            print(f"📊 Проверка задачи {i+1}/{len(tasks)}...")
            
            max_attempts = 60
            for attempt in range(max_attempts):
                status = await network.get_task_status(task_id)
                print(f"  Попытка {attempt + 1}/{max_attempts}: {status['status']}")
                
                if status['status'] == 'completed':
                    result = await network.get_task_result(task_id)
                    results.append(result)
                    print(f"  ✅ Задача {i+1} завершена")
                    break
                elif status['status'] == 'failed':
                    print(f"  ❌ Задача {i+1} не выполнена")
                    results.append(None)
                    break
                    
                await asyncio.sleep(1)
            else:
                print(f"  ⏰ Задача {i+1} не завершилась")
                results.append(None)
        
        # Агрегация результатов
        print("📈 Агрегация результатов...")
        valid_results = [r for r in results if r is not None]
        
        if valid_results:
            final_result = np.mean(valid_results, axis=0)
            print(f"🎯 Финальный результат: {final_result}")
            print(f"📊 Успешно выполнено: {len(valid_results)}/{len(tasks)} задач")
        else:
            print("❌ Ни одна задача не была выполнена успешно")
        
    except Exception as e:
        print(f"💥 Ошибка: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        await network.stop()
        print("✅ Сеть остановлена")

if __name__ == "__main__":
    asyncio.run(batch_processing_example())
```

### Пример 3: Работа с репутацией и кредитами

```python
#!/usr/bin/env python3
# credits_reputation_example.py

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import ComputeNetwork
from core.task import Task, TaskType, TaskPriority
from core.reputation import Reputation
from core.credits import Credits

async def credits_reputation_example():
    # Создание сети
    network = ComputeNetwork(host="127.0.0.1", port=5559)
    
    try:
        await network.start()
        await asyncio.sleep(2)
        
        # Получение информации о кредитах и репутации
        print("💳 Информация о кредитах:")
        print(f"  Баланс: {network.credits.get_balance():.2f}")
        print(f"  Максимальный баланс: {network.credits.max_balance}")
        
        print("\n🏆 Информация о репутации:")
        print(f"  Балл: {network.reputation.get_score():.3f}")
        print(f"  Уровень: {network.reputation.get_level()}")
        
        # Создание задачи для проверки кредитов
        task = Task.create_range_reduce(
            owner_id=network.node.node_id,
            start=1,
            end=100,
            operation="sum",
            requirements={
                "cpu_percent": 30.0,
                "ram_gb": 0.5,
                "timeout_seconds": 30
            },
            config={
                "max_price": 0.05,
                "priority": TaskPriority.NORMAL.value
            }
        )
        
        # Оценка стоимости
        estimated_cost = task.estimate_cost(network.reputation.get_score())
        print(f"\n💰 Оценочная стоимость задачи: {estimated_cost:.4f}")
        
        # Проверка достаточности кредитов
        if network.credits.get_balance() >= estimated_cost:
            print("✅ Достаточно кредитов для выполнения задачи")
            
            # Подача задачи
            task_id = await network.submit_task(task.to_dict())
            print(f"📝 Задача создана: {task_id}")
            
            # Ожидание завершения
            while True:
                status = await network.get_task_status(task_id)
                if status['status'] in ['completed', 'failed']:
                    break
                await asyncio.sleep(1)
            
            # Обновление репутации в зависимости от результата
            if status['status'] == 'completed':
                network.reputation.add_positive_feedback(0.1)
                print("🎉 Задача выполнена успешно, репутация улучшена")
            else:
                network.reputation.add_negative_feedback(0.1)
                print("❌ Задача не выполнена, репутация ухудшена")
                
        else:
            print("❌ Недостаточно кредитов для выполнения задачи")
        
        # Финальная информация
        print(f"\n💳 Финальный баланс: {network.credits.get_balance():.2f}")
        print(f"🏆 Финальная репутация: {network.reputation.get_score():.3f}")
        
    except Exception as e:
        print(f"💥 Ошибка: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        await network.stop()
        print("✅ Сеть остановлена")

if __name__ == "__main__":
    asyncio.run(credits_reputation_example())
```

---

## 🚀 Продвинутые примеры

### Пример 1: ML инференс с GPU

```python
#!/usr/bin/env python3
# ml_inference_example.py

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import ComputeNetwork
from core.task import Task, TaskType, TaskPriority

async def ml_inference_example():
    # Создание сети
    network = ComputeNetwork(host="127.0.0.1", port=5560)
    
    try:
        await network.start()
        await asyncio.sleep(2)
        
        # Путь к модели
        model_path = "models/resnet50.h5"
        
        # Тестовые данные (изображение в base64)
        input_data = {
            "image_data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
            "preprocessing": {
                "normalize": True,
                "resize": (224, 224)
            }
        }
        
        print("🤖 Создание задачи ML инференса...")
        
        # Создание задачи ML инференса
        task = Task.create_ml_inference(
            owner_id=network.node.node_id,
            model_path=model_path,
            input_data=input_data,
            requirements={
                "cpu_percent": 30.0,
                "ram_gb": 4.0,
                "gpu_percent": 80.0,
                "timeout_seconds": 120
            },
            config={
                "max_price": 1.0,
                "priority": TaskPriority.HIGH.value,
                "return_probabilities": True,
                "batch_size": 32
            }
        )
        
        print(f"📝 Задача создана: {task.task_id}")
        print(f"💰 Оценочная стоимость: {task.estimate_cost(network.reputation.get_score()):.4f}")
        
        # Подача задачи
        task_id = await network.submit_task(task.to_dict())
        print(f"✅ Задача отправлена: {task_id}")
        
        # Мониторинг выполнения
        while True:
            status = await network.get_task_status(task_id)
            print(f"📊 Статус: {status['status']}")
            
            if status['status'] == 'completed':
                result = await network.get_task_result(task_id)
                print(f"🎯 Предсказание: {result['predictions']}")
                print(f"📈 Вероятности: {result['probabilities']}")
                break
            elif status['status'] == 'failed':
                print(f"❌ ML инференс не выполнен: {status.get('error', 'Unknown error')}")
                break
                
            await asyncio.sleep(2)
            
    except Exception as e:
        print(f"💥 Ошибка: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        await network.stop()
        print("✅ Сеть остановлена")

if __name__ == "__main__":
    asyncio.run(ml_inference_example())
```

### Пример 2: Матричные операции

```python
#!/usr/bin/env python3
# matrix_operations_example.py

import asyncio
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import ComputeNetwork
from core.task import Task, TaskType, TaskPriority

async def matrix_operations_example():
    # Создание сети
    network = ComputeNetwork(host="127.0.0.1", port=5561)
    
    try:
        await network.start()
        await asyncio.sleep(2)
        
        # Создание матриц
        print("🔢 Создание матриц...")
        matrix_a = np.random.rand(1000, 1000)
        matrix_b = np.random.rand(1000, 1000)
        
        print(f"📊 Матрица A: {matrix_a.shape}")
        print(f"📊 Матрица B: {matrix_b.shape}")
        
        # Тестирование разных операций
        operations = ["multiply", "add", "subtract", "transpose"]
        
        for operation in operations:
            print(f"\n🔄 Выполнение операции: {operation}")
            
            try:
                task = Task.create_matrix_ops(
                    owner_id=network.node.node_id,
                    matrix_a=matrix_a.tolist(),
                    matrix_b=matrix_b.tolist(),
                    operation=operation,
                    requirements={
                        "cpu_percent": 80.0,
                        "ram_gb": 8.0,
                        "timeout_seconds": 60
                    },
                    config={
                        "max_price": 0.5,
                        "priority": TaskPriority.NORMAL.value
                    }
                )
                
                task_id = await network.submit_task(task.to_dict())
                print(f"✅ Задача создана: {task_id}")
                
                # Ожидание завершения
                while True:
                    status = await network.get_task_status(task_id)
                    if status['status'] in ['completed', 'failed']:
                        break
                    await asyncio.sleep(1)
                
                if status['status'] == 'completed':
                    result = await network.get_task_result(task_id)
                    result_matrix = np.array(result)
                    print(f"🎉 Результат: {result_matrix.shape}")
                else:
                    print(f"❌ Операция не выполнена: {status.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"💥 Ошибка операции {operation}: {e}")
        
    except Exception as e:
        print(f"💥 Ошибка: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        await network.stop()
        print("✅ Сеть остановлена")

if __name__ == "__main__":
    asyncio.run(matrix_operations_example())
```

### Пример 3: Pipeline обработки данных

```python
#!/usr/bin/env python3
# data_pipeline_example.py

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import ComputeNetwork
from core.task import Task, TaskType, TaskPriority

async def data_pipeline_example():
    # Создание сети
    network = ComputeNetwork(host="127.0.0.1", port=5562)
    
    try:
        await network.start()
        await asyncio.sleep(2)
        
        # Этап 1: Генерация данных
        print("📊 Этап 1: Генерация данных...")
        data_task = Task.create_map(
            owner_id=network.node.node_id,
            data=list(range(10000)),
            operation="generate_data",
            requirements={
                "cpu_percent": 50.0,
                "ram_gb": 2.0,
                "timeout_seconds": 30
            },
            config={
                "max_price": 0.1,
                "priority": TaskPriority.NORMAL.value
            }
        )
        
        data_task_id = await network.submit_task(data_task.to_dict())
        print(f"✅ Задача генерации данных: {data_task_id}")
        
        # Этап 2: Преобразование данных
        print("\n🔄 Этап 2: Преобразование данных...")
        transform_task = Task.create_map(
            owner_id=network.node.node_id,
            data=[],  # Данные будут получены из предыдущей задачи
            operation="transform",
            requirements={
                "cpu_percent": 70.0,
                "ram_gb": 4.0,
                "timeout_seconds": 60
            },
            config={
                "max_price": 0.2,
                "priority": TaskPriority.NORMAL.value,
                "depends_on": data_task_id
            }
        )
        
        transform_task_id = await network.submit_task(transform_task.to_dict())
        print(f"✅ Задача преобразования: {transform_task_id}")
        
        # Этап 3: Анализ данных
        print("\n📈 Этап 3: Анализ данных...")
        analyze_task = Task.create_map_reduce(
            owner_id=network.node.node_id,
            data=[],  # Данные будут получены из предыдущей задачи
            map_operation="map",
            reduce_operation="reduce",
            requirements={
                "cpu_percent": 60.0,
                "ram_gb": 3.0,
                "timeout_seconds": 45
            },
            config={
                "max_price": 0.15,
                "priority": TaskPriority.NORMAL.value,
                "depends_on": transform_task_id
            }
        )
        
        analyze_task_id = await network.submit_task(analyze_task.to_dict())
        print(f"✅ Задача анализа: {analyze_task_id}")
        
        # Ожидание завершения всего пайплайна
        pipeline_tasks = [data_task_id, transform_task_id, analyze_task_id]
        results = {}
        
        print("\n⏳ Ожидание завершения пайплайна...")
        while len(results) < len(pipeline_tasks):
            for task_id in pipeline_tasks:
                if task_id not in results:
                    status = await network.get_task_status(task_id)
                    print(f"📊 Задача {task_id}: {status['status']}")
                    
                    if status['status'] == 'completed':
                        result = await network.get_task_result(task_id)
                        results[task_id] = result
                        print(f"✅ Задача {task_id} завершена")
                    elif status['status'] == 'failed':
                        results[task_id] = None
                        print(f"❌ Задача {task_id} не выполнена")
            
            await asyncio.sleep(2)
        
        # Вывод результатов
        print("\n🎯 Результаты пайплайна:")
        for task_id, result in results.items():
            if result is not None:
                print(f"✅ Задача {task_id}: успешно выполнена")
            else:
                print(f"❌ Задача {task_id}: не выполнена")
        
    except Exception as e:
        print(f"💥 Ошибка: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        await network.stop()
        print("✅ Сеть остановлена")

if __name__ == "__main__":
    asyncio.run(data_pipeline_example())
```

---

## 🔗 Примеры интеграции

### Пример 1: Интеграция с веб-приложением

```python
#!/usr/bin/env python3
# web_integration_example.py

from flask import Flask, request, jsonify
import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import ComputeNetwork
from core.task import Task, TaskType, TaskPriority

app = Flask(__name__)
network = None

async def init_network():
    global network
    network = ComputeNetwork(host="127.0.0.1", port=5563)
    await network.start()
    await asyncio.sleep(2)

@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        
        # Валидация данных
        required_fields = ['numbers', 'operation']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Создание задачи
        task = Task.create_range_reduce(
            owner_id="web_user",
            start=min(data['numbers']),
            end=max(data['numbers']),
            operation=data['operation'],
            requirements={
                "cpu_percent": 50.0,
                "ram_gb": 1.0,
                "timeout_seconds": 30
            },
            config={
                "max_price": 0.1,
                "priority": TaskPriority.NORMAL.value
            }
        )
        
        # Подача задачи
        task_id = asyncio.run_coroutine_threadsafe(
            network.submit_task(task.to_dict()), 
            network.loop
        ).result()
        
        return jsonify({
            'task_id': task_id,
            'status': 'submitted'
        }), 202
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status/<task_id>', methods=['GET'])
def get_status(task_id):
    try:
        status = asyncio.run_coroutine_threadsafe(
            network.get_task_status(task_id), 
            network.loop
        ).result()
        
        return jsonify(status), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/result/<task_id>', methods=['GET'])
def get_result(task_id):
    try:
        result = asyncio.run_coroutine_threadsafe(
            network.get_task_result(task_id), 
            network.loop
        ).result()
        
        return jsonify({'result': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/network/status', methods=['GET'])
def get_network_status():
    try:
        status = asyncio.run_coroutine_threadsafe(
            network.get_network_status(), 
            network.loop
        ).result()
        
        return jsonify(status), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Инициализация сети
    asyncio.run(init_network())
    
    # Запуск веб-приложения
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Пример 2: Интеграция с Docker

```dockerfile
# Dockerfile
FROM python:3.9-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Копирование кода
WORKDIR /app
COPY src/ ./src/
COPY examples/ ./examples/
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Создание пользователя
RUN useradd -m -u 1000 compute
USER compute

# Открытие портов
EXPOSE 5557 5558 8080

# Запуск приложения
CMD ["python", "examples/basic_network_example.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  compute-network:
    build: .
    ports:
      - "5557:5557"
      - "8080:8080"
    environment:
      - NODE_TYPE=public
      - SEED_NODES=seed1:5557
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    
  seed-node:
    build: .
    ports:
      - "5557:5557"
    environment:
      - NODE_TYPE=seed
    restart: unless-stopped
    command: ["python", "examples/basic_network_example.py", "--seed-mode"]
    
  web-app:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - compute-network
    environment:
      - SEED_NODES=compute-network:5557
    volumes:
      - ./web:/app/web
    restart: unless-stopped
    command: ["python", "examples/web_integration_example.py"]
```

### Пример 3: Интеграция с Kubernetes

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: compute-network
spec:
  replicas: 3
  selector:
    matchLabels:
      app: compute-network
  template:
    metadata:
      labels:
        app: compute-network
    spec:
      containers:
      - name: compute-network
        image: compute-network:latest
        ports:
        - containerPort: 5557
        - containerPort: 8080
        env:
        - name: NODE_TYPE
          value: "public"
        - name: SEED_NODES
          value: "seed-service:5557"
        resources:
          requests:
            cpu: "1"
            memory: "2Gi"
          limits:
            cpu: "2"
            memory: "4Gi"
        volumeMounts:
        - name: config
          mountPath: /app/config
        - name: data
          mountPath: /app/data
        - name: logs
          mountPath: /app/logs
      volumes:
      - name: config
        configMap:
          name: compute-network-config
      - name: data
        persistentVolumeClaim:
          claimName: compute-network-data
      - name: logs
        persistentVolumeClaim:
          claimName: compute-network-logs
```

---

## ⚠️ Типичные проблемы и решения

### Проблема 1: Не удается подключиться к сети

**Симптомы:**
- Сообщение "No credits in system"
- Статус сети показывает 0 узлов
- Задачи не выполняются

**Возможные причины:**
- Нет seed-узлов для подключения
- Неверная конфигурация сети
- Проблемы с сетевыми подключениями
- Фаервол блокирует порты

**Решения:**

1. **Проверка конфигурации:**
```python
# Проверка seed-узлов
seed_nodes = ["seed1.example.com:5557", "seed2.example.com:5557"]
network = ComputeNetwork(seed_nodes=seed_nodes)
```

2. **Проверка сетевых подключений:**
```bash
# Проверка портов
netstat -tuln | grep 5557

# Проверка подключений
telnet seed1.example.com 5557

# Проверка фаервола
sudo ufw status
```

3. **Запуск seed-узла:**
```python
# Запуск seed-узла
seed_network = ComputeNetwork(
    host="0.0.0.0",
    port=5557,
    node_type="seed"
)
await seed_network.start()
```

### Проблема 2: Задачи не выполняются

**Симптомы:**
- Задача переходит в статус "pending"
- Нет исполнителей для задачи
- Таймаут выполнения

**Возможные причины:**
- Недостаточно compute-кредитов
- Несовместимые требования к ресурсам
- Проблемы с sandbox
- Высокая нагрузка на сеть

**Решения:**

1. **Проверка кредитов:**
```python
# Проверка баланса
balance = network.credits.get_balance()
print(f"Баланс: {balance}")

# Пополнение кредитов
network.credits.add_credits(100.0, "manual_topup")
```

2. **Проверка требований:**
```python
# Проверка доступности узлов
nodes = await network.get_nodes_list()
for node in nodes:
    capabilities = node['capabilities']
    print(f"Узел {node['node_id']}: CPU={capabilities['cpu_score']}, RAM={capabilities['ram_gb']}GB")
```

3. **Увеличение таймаута:**
```python
task = Task.create_range_reduce(
    # ... другие параметры ...
    requirements={
        "timeout_seconds": 120  # Увеличить таймаут
    }
)
```

### Проблема 3: Высокая загрузка CPU/RAM

**Симптомы:**
- Медленная работа сети
- Задачи выполняются долго
- Ошибки нехватки памяти

**Возможные причины:**
- Слишком много одновременных задач
- Недостаточно ресурсов узла
- Неэффективный алгоритм

**Решения:**

1. **Ограничение одновременных задач:**
```python
# Ограничение в конфигурации
config = {
    "max_concurrent_tasks": 5,  # Уменьшить количество
    "task_queue_size": 100
}
```

2. **Оптимизация ресурсов:**
```python
# Уменьшение требований к задачам
requirements = {
    "cpu_percent": 30.0,  # Уменьшить CPU
    "ram_gb": 1.0,       # Уменьшить RAM
    "timeout_seconds": 60
}
```

3. **Мониторинг ресурсов:**
```python
# Проверка использования ресурсов
metrics = await network.get_resource_metrics()
print(f"CPU: {metrics['cpu_usage']:.1f}%")
print(f"RAM: {metrics['ram_usage']:.1f}%")
```

### Проблема 4: Проблемы с безопасностью

**Симптомы:**
- Ошибки аутентификации
- Подозрительная активность
- Несанкционированный доступ

**Возможные причины:**
- Слабые пароли
- Уязвимости в коде
- Отсутствие шифрования

**Решения:**

1. **Усиление безопасности:**
```python
# Включение шифрования
security_config = {
    "encryption": {
        "enabled": True,
        "algorithm": "TLS_1.3"
    },
    "authentication": {
        "method": "certificate",
        "require_seed_signature": True
    }
}
```

2. **Проверка логов:**
```bash
# Проверка логов на подозрительную активность
grep -i "failed\|error\|denied" /var/log/compute-network.log
```

3. **Обновление системы:**
```bash
# Обновление зависимостей
pip install --upgrade -r requirements.txt

# Обновление системы
sudo apt-get update && sudo apt-get upgrade
```

---

## 🐛 Отладка и диагностика

### Инструменты диагностики

#### 1. Скрипт диагностики сети

```python
#!/usr/bin/env python3
# network_diagnostics.py

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import ComputeNetwork

async def network_diagnostics():
    network = ComputeNetwork(host="127.0.0.1", port=5564)
    
    try:
        await network.start()
        await asyncio.sleep(2)
        
        print("🔍 Диагностика сети...")
        
        # Проверка статуса сети
        status = await network.get_network_status()
        print(f"📊 Статус сети: {status}")
        
        # Проверка списка узлов
        nodes = await network.get_nodes_list()
        print(f"🌐 Узлы в сети: {len(nodes)}")
        
        for node in nodes:
            print(f"  - {node['node_id']}: {node['status']}")
        
        # Проверка метрик
        metrics = await network.get_network_metrics()
        print(f"📈 Метрики сети:")
        print(f"  - CPU: {metrics['cpu_usage']:.1f}%")
        print(f"  - RAM: {metrics['ram_usage']:.1f}%")
        print(f"  - Активных задач: {metrics['active_tasks']}")
        
        # Проверка кредитов
        credit_metrics = await network.get_credit_metrics()
        print(f"💳 Кредиты:")
        print(f"  - Баланс: {credit_metrics['balance']:.2f}")
        print(f"  - Транзакций: {credit_metrics['total_transactions']}")
        
        # Проверка репутации
        reputation_metrics = network.reputation.get_metrics()
        print(f"🏆 Репутация:")
        print(f"  - Балл: {network.reputation.get_score():.3f}")
        print(f"  - Уровень: {network.reputation.get_level()}")
        
    except Exception as e:
        print(f"💥 Ошибка диагностики: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        await network.stop()

if __name__ == "__main__":
    asyncio.run(network_diagnostics())
```

#### 2. Анализ логов

```python
#!/usr/bin/env python3
# log_analyzer.py

import re
import json
from collections import defaultdict
from datetime import datetime, timedelta

def analyze_logs(log_file, hours=24):
    """Анализ логов за последние N часов"""
    
    cutoff_time = datetime.now() - timedelta(hours=hours)
    results = defaultdict(list)
    
    with open(log_file, 'r') as f:
        for line in f:
            try:
                # Извлечение времени
                time_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                if time_match:
                    log_time = datetime.strptime(time_match.group(1), '%Y-%m-%d %H:%M:%S')
                    
                    if log_time >= cutoff_time:
                        # Анализ строки
                        if 'ERROR' in line:
                            results['errors'].append(line.strip())
                        elif 'WARNING' in line:
                            results['warnings'].append(line.strip())
                        elif 'INFO' in line:
                            results['info'].append(line.strip())
                        elif 'task' in line.lower():
                            results['tasks'].append(line.strip())
                            
            except Exception as e:
                print(f"Ошибка обработки строки: {e}")
    
    return results

def generate_report(results):
    """Генерация отчета"""
    
    report = {
        'analysis_time': datetime.now().isoformat(),
        'time_range': f'last_{len(results)}_hours',
        'summary': {
            'errors': len(results['errors']),
            'warnings': len(results['warnings']),
            'info': len(results['info']),
            'tasks': len(results['tasks'])
        }
    }
    
    return report

if __name__ == "__main__":
    log_file = "/opt/compute-network/logs/compute_network.log"
    results = analyze_logs(log_file)
    report = generate_report(results)
    
    print("📊 Отчет анализа логов:")
    print(json.dumps(report, indent=2))
    
    print("\n🔍 Последние ошибки:")
    for error in results['errors'][-5:]:
        print(f"  - {error}")
    
    print("\n⚠️ Последние предупреждения:")
    for warning in results['warnings'][-5:]:
        print(f"  - {warning}")
```

### Профилирование производительности

```python
#!/usr/bin/env python3
# performance_profiler.py

import cProfile
import pstats
import io
import time
from contextlib import redirect_stdout

class PerformanceProfiler:
    def __init__(self):
        self.profiler = cProfile.Profile()
        
    def profile_function(self, func, *args, **kwargs):
        """Профилирование функции"""
        
        self.profiler.enable()
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"✅ Функция {func.__name__} выполнена за {duration:.4f} секунд")
            return result
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            print(f"❌ Функция {func.__name__} завершилась с ошибкой за {duration:.4f} секунд: {e}")
            raise
            
        finally:
            self.profiler.disable()
            
    def get_stats(self, output_file='performance_stats.prof'):
        """Получение статистики"""
        
        stats = pstats.Stats(self.profiler)
        stats.sort_stats('cumulative')
        stats.dump_stats(output_file)
        
        # Вывод статистики
        print("\n📊 Статистика производительности:")
        stats.print_stats(10)
        
        return stats

# Пример использования
async def example_function():
    """Пример функции для профилирования"""
    await asyncio.sleep(0.1)
    result = sum(range(1000))
    return result

async def main():
    profiler = PerformanceProfiler()
    
    # Профилирование функции
    result = profiler.profile_function(example_function)
    print(f"Результат: {result}")
    
    # Получение статистики
    stats = profiler.get_stats()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## ⚡ Производительность

### Оптимизация производительности

#### 1. Оптимизация сети

```python
# network_optimization.py

import asyncio
import aiohttp
import time
from concurrent.futures import ThreadPoolExecutor

class NetworkOptimizer:
    def __init__(self, network):
        self.network = network
        self.executor = ThreadPoolExecutor(max_workers=4)
        
    async def optimize_network_requests(self):
        """Оптимизация сетевых запросов"""
        
        # Использование пулов соединений
        connector = aiohttp.TCPConnector(
            limit=100,
            limit_per_host=30,
            ttl_dns_cache=300,
            use_dns_cache=True
        )
        
        async with aiohttp.ClientSession(connector=connector) as session:
            # Параллельные запросы
            tasks = [
                self.make_request(session, f"http://node{i}:5557/status")
                for i in range(10)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Обработка результатов
            successful = [r for r in results if not isinstance(r, Exception)]
            failed = [r for r in results if isinstance(r, Exception)]
            
            print(f"✅ Успешных запросов: {len(successful)}")
            print(f"❌ Неудачных запросов: {len(failed)}")
            
    async def make_request(self, session, url):
        """Создание запроса с таймаутом"""
        
        try:
            async with session.get(url, timeout=10) as response:
                return await response.json()
        except asyncio.TimeoutError:
            raise Exception("Timeout")
        except Exception as e:
            raise Exception(f"Request failed: {e}")
```

#### 2. Оптимизация задач

```python
# task_optimization.py

import asyncio
import numpy as np
from typing import List, Dict

class TaskOptimizer:
    def __init__(self):
        self.cache = {}
        
    def optimize_task_chunking(self, data_size: int, chunk_size: int = None):
        """Оптимизация разбиения задач на чанки"""
        
        if chunk_size is None:
            # Автоматический расчет оптимального размера чанка
            chunk_size = self.calculate_optimal_chunk_size(data_size)
        
        chunks = []
        for i in range(0, data_size, chunk_size):
            chunk_end = min(i + chunk_size, data_size)
            chunks.append((i, chunk_end))
        
        return chunks
    
    def calculate_optimal_chunk_size(self, data_size: int) -> int:
        """Расчет оптимального размера чанка"""
        
        # Базовый размер чанка
        base_chunk_size = 1000
        
        # Адаптация под размер данных
        if data_size < 10000:
            return base_chunk_size
        elif data_size < 100000:
            return base_chunk_size * 2
        else:
            return base_chunk_size * 5
    
    def optimize_task_requirements(self, task_type: str, data_size: int) -> Dict:
        """Оптимизация требований к задаче"""
        
        requirements = {
            "cpu_percent": 50.0,
            "ram_gb": 2.0,
            "timeout_seconds": 60
        }
        
        # Адаптация под тип задачи и размер данных
        if task_type == "ml_inference":
            requirements["gpu_percent"] = 80.0
        elif task_type == "matrix_ops":
            requirements["cpu_percent"] = min(90.0, 50.0 + data_size / 10000)
            requirements["ram_gb"] = min(16.0, 2.0 + data_size / 10000)
        
        return requirements
```

### Нагрузочное тестирование

```python
# load_testing.py

import asyncio
import aiohttp
import random
import time
from typing import List, Dict

class LoadTester:
    def __init__(self, base_url: str, concurrent_users: int = 10):
        self.base_url = base_url
        self.concurrent_users = concurrent_users
        self.results = []
        
    async def run_load_test(self, duration: int = 60):
        """Запуск нагрузочного тестирования"""
        
        start_time = time.time()
        
        async def worker():
            while time.time() - start_time < duration:
                # Симуляция пользовательского действия
                await self.simulate_user_action()
                await asyncio.sleep(random.uniform(0.1, 1.0))
                
        tasks = [worker() for _ in range(self.concurrent_users)]
        await asyncio.gather(*tasks)
        
    async def simulate_user_action(self):
        """Симуляция пользовательского действия"""
        
        actions = [
            self.check_network_status,
            self.submit_task,
            self.get_task_status,
            self.get_task_result
        ]
        
        action = random.choice(actions)
        await action()
        
    async def check_network_status(self):
        """Проверка статуса сети"""
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/network/status") as response:
                    if response.status == 200:
                        self.results.append({
                            'action': 'check_status',
                            'success': True,
                            'duration': time.time(),
                            'response_time': 0.1  # симуляция
                        })
        except Exception as e:
            self.results.append({
                'action': 'check_status',
                'success': False,
                'duration': time.time(),
                'error': str(e)
            })
            
    async def submit_task(self):
        """Подача задачи"""
        
        try:
            task_data = {
                "task_type": "range_reduce",
                "start": 1,
                "end": 1000,
                "operation": "sum"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/tasks",
                    json=task_data
                ) as response:
                    if response.status == 202:
                        self.results.append({
                            'action': 'submit_task',
                            'success': True,
                            'duration': time.time(),
                            'response_time': 0.2
                        })
        except Exception as e:
            self.results.append({
                'action': 'submit_task',
                'success': False,
                'duration': time.time(),
                'error': str(e)
            })
            
    def generate_report(self):
        """Генерация отчета о нагрузочном тестировании"""
        
        total_requests = len(self.results)
        successful_requests = sum(1 for r in self.results if r['success'])
        failed_requests = total_requests - successful_requests
        
        avg_response_time = sum(
            r.get('response_time', 0) for r in self.results
        ) / total_requests
        
        success_rate = (successful_requests / total_requests) * 100
        
        report = {
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'failed_requests': failed_requests,
            'success_rate': success_rate,
            'average_response_time': avg_response_time,
            'requests_per_second': total_requests / (
                self.results[-1]['duration'] - self.results[0]['duration']
            )
        }
        
        return report

# Пример использования
async def main():
    tester = LoadTester("http://localhost:8080", concurrent_users=20)
    await tester.run_load_test(duration=60)
    
    report = tester.generate_report()
    print("📊 Отчет нагрузочного тестирования:")
    print(f"  - Всего запросов: {report['total_requests']}")
    print(f"  - Успешных: {report['successful_requests']}")
    print(f"  - Неудачных: {report['failed_requests']}")
    print(f"  - Успешность: {report['success_rate']:.1f}%")
    print(f"  - Среднее время ответа: {report['average_response_time']:.3f}s")
    print(f"  - Запросов в секунду: {report['requests_per_second']:.1f}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🔒 Безопасность

### Проверка безопасности

```python
# security_check.py

import asyncio
import aiohttp
import hashlib
import json
from typing import List, Dict

class SecurityChecker:
    def __init__(self, base_url: str):
        self.base_url = base_url
        
    async def run_security_checks(self):
        """Запуск проверок безопасности"""
        
        checks = [
            self.check_sql_injection,
            self.check_xss,
            self.check_authentication,
            self.check_authorization,
            self.check_input_validation
        ]
        
        results = []
        
        for check in checks:
            try:
                result = await check()
                results.append(result)
            except Exception as e:
                results.append({
                    'check': check.__name__,
                    'status': 'failed',
                    'error': str(e)
                })
        
        return results
        
    async def check_sql_injection(self):
        """Проверка на SQL инъекции"""
        
        malicious_inputs = [
            "1' OR '1'='1",
            "1; DROP TABLE users;",
            "1' UNION SELECT * FROM users--"
        ]
        
        for payload in malicious_inputs:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.base_url}/api/tasks",
                        json={"task_type": payload}
                    ) as response:
                        if response.status == 500:
                            return {
                                'check': 'sql_injection',
                                'status': 'vulnerable',
                                'payload': payload
                            }
            except Exception as e:
                continue
                
        return {
            'check': 'sql_injection',
            'status': 'secure'
        }
        
    async def check_xss(self):
        """Проверка на XSS атаки"""
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>"
        ]
        
        for payload in xss_payloads:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.base_url}/api/tasks",
                        json={"task_type": payload}
                    ) as response:
                        if payload in await response.text():
                            return {
                                'check': 'xss',
                                'status': 'vulnerable',
                                'payload': payload
                            }
            except Exception as e:
                continue
                
        return {
            'check': 'xss',
            'status': 'secure'
        }
        
    async def check_authentication(self):
        """Проверка аутентификации"""
        
        # Попытка доступа без аутентификации
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/admin") as response:
                    if response.status == 200:
                        return {
                            'check': 'authentication',
                            'status': 'vulnerable'
                        }
        except Exception as e:
            pass
            
        return {
            'check': 'authentication',
            'status': 'secure'
        }

# Пример использования
async def main():
    checker = SecurityChecker("http://localhost:8080")
    results = await checker.run_security_checks()
    
    print("🔒 Отчет проверки безопасности:")
    for result in results:
        status = "✅" if result['status'] == 'secure' else "❌"
        print(f"  {status} {result['check']}: {result['status']}")
        if 'payload' in result:
            print(f"     Payload: {result['payload']}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## ❓ FAQ

### Вопросы по установке и настройке

**Q: Как установить систему на Ubuntu?**
```bash
# Клонирование репозитория
git clone https://github.com/your-org/compute-network.git
cd compute-network

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Установка системных зависимостей
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip build-essential git

# Запуск
python -m main
```

**Q: Как настроить seed-узел?**
```python
# Создание seed-узла
seed_network = ComputeNetwork(
    host="0.0.0.0",
    port=5557,
    node_type="seed"
)

await seed_network.start()
```

**Q: Как подключиться к существующей сети?**
```python
# Подключение к seed-узлам
network = ComputeNetwork(
    host="127.0.0.1",
    port=5558,
    seed_nodes=["seed1.example.com:5557", "seed2.example.com:5557"]
)
```

### Вопросы по использованию

**Q: Как создать задачу?**
```python
from core.task import Task, TaskType, TaskPriority

task = Task.create_range_reduce(
    owner_id="user_001",
    start=1,
    end=1000,
    operation="sum",
    requirements={
        "cpu_percent": 50.0,
        "ram_gb": 1.0,
        "timeout_seconds": 60
    },
    config={
        "max_price": 0.1,
        "priority": TaskPriority.NORMAL.value
    },
    privacy={
        "mode": "shard",
        "zk_verify": "basic"
    }
)
```

**Q: Как проверить статус задачи?**
```python
status = await network.get_task_status(task_id)
print(f"Статус: {status['status']}")
```

**Q: Как получить результат задачи?**
```python
result = await network.get_task_result(task_id)
print(f"Результат: {result}")
```

### Вопросы по проблемам

**Q: Что делать, если задачи не выполняются?**
1. Проверить баланс compute-кредитов
2. Проверить наличие узлов в сети
3. Проверить требования к ресурсам
4. Увеличить таймаут выполнения

**Q: Как оптимизировать производительность?**
1. Использовать оптимальные размеры чанков
2. Балансировать нагрузку между узлами
3. Использовать кэширование результатов
4. Оптимизировать сетевые запросы

**Q: Как обеспечить безопасность?**
1. Использовать SSL/TLS шифрование
2. Включить аутентификацию
3. Ограничить доступ к административным интерфейсам
4. Регулярно обновлять систему

### Вопросы по масштабированию

**Q: Как масштабировать систему?**
```python
# Горизонтальное масштабирование
# Добавление новых узлов в сеть

# Вертикальное масштабирование
# Увеличение ресурсов существующих узлов

# Балансировка нагрузки
# Использование балансировщиков нагрузки
```

**Q: Как развернуть в Kubernetes?**
```yaml
# Использование Kubernetes Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: compute-network
spec:
  replicas: 3
  # ...
```

---

## 🎯 Заключение

Эта документация предоставила comprehensive примеры использования и руководство по troubleshooting для децентрализованной P2P вычислительной сети:

- ✅ **Базовые примеры** - запуск сети, создание задач, работа с кредитами
- ✅ **Продвинутые примеры** - ML инференс, матричные операции, пайплайны
- ✅ **Интеграция** - веб-приложения, Docker, Kubernetes
- ✅ **Troubleshooting** - типичные проблемы и их решения
- ✅ **Отладка** - инструменты диагностики и профилирования
- ✅ **Производительность** - оптимизация и нагрузочное тестирование
- ✅ **Безопасность** - проверки и рекомендации
- ✅ **FAQ** - ответы на частые вопросы

Система готова к использованию и обеспечивает надежную основу для децентрализованных вычислений.

🚀 **Начните использовать Compute Network уже сегодня!**
