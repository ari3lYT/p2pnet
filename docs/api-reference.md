# 📚 API Справочник

## 📋 Содержание

- [Обзор API](#обзор-api)
- [Основные классы](#основные-классы)
- [Сеть (ComputeNetwork)](#сеть-computenetwork)
- [Узел (Node)](#узел-node)
- [Задачи (Task)](#задачи-task)
- [Compute-кредиты (Credits)](#compute-кредиты-credits)
- [Репутация (Reputation)](#репутация-reputation)
- [Sandbox (Sandbox)](#sandbox-sandbox)
- [Примеры использования](#примеры-использования)
- [Обработка ошибок](#обработка-ошибок)
- [WebSocket API](#websocket-api)

---

## 🎯 Обзор API

API децентрализованной P2P вычислительной сети предоставляет программный интерфейс для взаимодействия с сетью, управления задачами, отслеживания выполнения и управления ресурсами.

### Основные принципы API

- **Асинхронность** - все методы API асинхронны и используют `async/await`
- **Обработка ошибок** - исключения используются для ошибок, а не для обычного потока
- **Валидация данных** - автоматическая валидация входных данных
- **Типизация** - полная типизация с использованием Python type hints
- **Документация** - встроенная документация и примеры

### Структура API

```
src/
├── main.py              # Основной класс ComputeNetwork
├── core/
│   ├── node.py          # Класс Node
│   ├── task.py          # Класс Task
│   ├── credits.py       # Класс Credits
│   ├── reputation.py    # Класс Reputation
│   └── ...
├── sandbox/
│   ├── execution.py     # Sandbox выполнение
│   └── ...
├── pricing/
│   ├── dynamic.py       # Динамическое ценообразование
│   └── ...
└── network/
    ├── discovery.py     # Обнаружение узлов
    ├── routing.py       # Маршрутизация
    └── protocol.py      # Протоколы
```

---

## 🔧 Основные классы

### Импорт основных классов

```python
from src.main import ComputeNetwork
from src.core.node import Node, Capabilities
from src.core.task import Task, TaskType, TaskPriority, TaskStatus
from src.core.credits import Credits, CreditTransaction
from src.core.reputation import Reputation
from src.sandbox.execution import Sandbox, SandboxType
from src.pricing.dynamic import PricingEngine
```

---

## 🌐 Сеть (ComputeNetwork)

Основной класс для взаимодействия с P2P сетью.

### Конструктор

```python
class ComputeNetwork:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 5557,
        node_type: str = "client",
        seed_nodes: Optional[List[str]] = None,
        config_path: Optional[str] = None,
        log_level: str = "INFO"
    ):
        """
        Инициализация вычислительной сети
        
        Args:
            host: Адрес для прослушивания
            port: Порт для прослушивания
            node_type: Тип узла (client, public, seed)
            seed_nodes: Список seed-узлов для подключения
            config_path: Путь к файлу конфигурации
            log_level: Уровень логирования
        """
```

### Основные методы

#### Управление сетью

```python
async def start(self) -> None:
    """Запуск сети"""
    
async def stop(self) -> None:
    """Остановка сети"""
    
async def restart(self) -> None:
    """Перезапуск сети"""
    
async def get_network_status(self) -> Dict[str, Any]:
    """Получение статуса сети"""
    
async def get_node_info(self) -> Dict[str, Any]:
    """Получение информации об узле"""
```

#### Управление задачами

```python
async def submit_task(self, task_data: Dict[str, Any]) -> str:
    """
    Подача задачи в сеть
    
    Args:
        task_data: Данные задачи
        
    Returns:
        task_id: Уникальный идентификатор задачи
    """
    
async def get_task_status(self, task_id: str) -> Dict[str, Any]:
    """
    Получение статуса задачи
    
    Args:
        task_id: Идентификатор задачи
        
    Returns:
        status: Статус задачи и метрики
    """
    
async def cancel_task(self, task_id: str) -> bool:
    """
    Отмена задачи
    
    Args:
        task_id: Идентификатор задачи
        
    Returns:
        success: Успешность отмены
    """
    
async def get_task_result(self, task_id: str) -> Any:
    """
    Получение результата задачи
    
    Args:
        task_id: Идентификатор задачи
        
    Returns:
        result: Результат выполнения
    """
```

#### Управление узлами

```python
async def get_nodes_list(self) -> List[Dict[str, Any]]:
    """Получение списка узлов в сети"""
    
async def get_node_details(self, node_id: str) -> Dict[str, Any]:
    """
    Получение деталей узла
    
    Args:
        node_id: Идентификатор узла
        
    Returns:
        details: Детальная информация об узле
    """
    
async def connect_to_node(self, node_id: str) -> bool:
    """
    Подключение к узлу
    
    Args:
        node_id: Идентификатор узла
        
    Returns:
        success: Успешность подключения
    """
    
async def disconnect_from_node(self, node_id: str) -> bool:
    """
    Отключение от узла
    
    Args:
        node_id: Идентификатор узла
        
    Returns:
        success: Успешность отключения
    """
```

#### Мониторинг и статистика

```python
async def get_network_metrics(self) -> Dict[str, Any]:
    """Получение метрик сети"""
    
async def get_task_metrics(self) -> Dict[str, Any]:
    """Получение метрик задач"""
    
async def get_resource_metrics(self) -> Dict[str, Any]:
    """Получение метрик использования ресурсов"""
    
async def get_credit_metrics(self) -> Dict[str, Any]:
    """Получение метрик кредитов"""
```

### Пример использования

```python
import asyncio
from src.main import ComputeNetwork
from src.core.task import Task, TaskType, TaskPriority

async def main():
    # Создание сети
    network = ComputeNetwork(host="127.0.0.1", port=5557)
    
    try:
        # Запуск сети
        await network.start()
        await asyncio.sleep(2)
        
        print(f"🆔 Node ID: {network.node.node_id}")
        
        # Создание задачи
        task_data = {
            "task_type": "range_reduce",
            "owner_id": network.node.node_id,
            "requirements": {
                "cpu_percent": 50.0,
                "ram_gb": 0.5,
                "timeout_seconds": 30
            },
            "config": {
                "operation": "sum",
                "start": 1,
                "end": 1000,
                "max_price": 0.1,
                "priority": TaskPriority.NORMAL.value
            }
        }
        
        # Подача задачи
        task_id = await network.submit_task(task_data)
        print(f"✅ Задача создана: {task_id}")
        
        # Ожидание завершения
        while True:
            status = await network.get_task_status(task_id)
            print(f"📊 Статус: {status['status']}")
            
            if status['status'] in ['completed', 'failed']:
                break
                
            await asyncio.sleep(2)
        
        # Получение результата
        if status['status'] == 'completed':
            result = await network.get_task_result(task_id)
            print(f"🎉 Результат: {result}")
        
    finally:
        await network.stop()

asyncio.run(main())
```

---

## 🖥️ Узел (Node)

Класс, представляющий узел в сети.

### Конструктор

```python
class Node:
    def __init__(
        self,
        node_id: str,
        host: str,
        port: int,
        capabilities: Optional[Capabilities] = None,
        node_type: str = "client"
    ):
        """
        Инициализация узла
        
        Args:
            node_id: Уникальный идентификатор узла
            host: Адрес узла
            port: Порт узла
            capabilities: Возможности узла
            node_type: Тип узла
        """
```

### Основные методы

#### Управление узлом

```python
async def start(self) -> None:
    """Запуск узла"""
    
async def stop(self) -> None:
    """Остановка узла"""
    
async def restart(self) -> None:
    """Перезапуск узла"""
    
async def get_status(self) -> Dict[str, Any]:
    """Получение статуса узла"""
```

#### Управление возможностями

```python
def update_capabilities(self, capabilities: Dict[str, Any]) -> None:
    """
    Обновление возможностей узла
    
    Args:
        capabilities: Новые возможности
    """
    
def get_current_load(self) -> Dict[str, float]:
    """Получение текущей загрузки"""
    
def is_available_for_task(self, task_requirements: Dict[str, Any]) -> bool:
    """
    Проверка доступности для задачи
    
    Args:
        task_requirements: Требования к задаче
        
    Returns:
        available: Доступен ли узел
    """
```

#### Управление связями

```python
async def connect_to_peer(self, peer_id: str) -> bool:
    """
    Подключение к узлу-равному
    
    Args:
        peer_id: Идентификатор узла
        
    Returns:
        success: Успешность подключения
    """
    
async def disconnect_from_peer(self, peer_id: str) -> bool:
    """
    Отключение от узла-равного
    
    Args:
        peer_id: Идентификатор узла
        
    Returns:
        success: Успешность отключения
    """
    
def get_peer_list(self) -> List[Dict[str, Any]]:
    """Получение списка связанных узлов"""
```

### Пример использования

```python
from src.core.node import Node, Capabilities

async def node_example():
    # Создание возможностей узла
    capabilities = Capabilities(
        cpu_score=8.0,
        ram_gb=16.0,
        disk_gb=500.0,
        gpu_score=2.0,
        max_concurrent_tasks=20
    )
    
    # Создание узла
    node = Node(
        node_id="node-001",
        host="192.168.1.100",
        port=5557,
        capabilities=capabilities,
        node_type="public"
    )
    
    try:
        # Запуск узла
        await node.start()
        
        # Получение статуса
        status = await node.get_status()
        print(f"📊 Статус узла: {status}")
        
        # Проверка доступности
        task_requirements = {
            "cpu_percent": 30.0,
            "ram_gb": 2.0,
            "timeout_seconds": 60
        }
        
        available = node.is_available_for_task(task_requirements)
        print(f"✅ Доступность для задачи: {available}")
        
    finally:
        await node.stop()
```

---

## 📋 Задачи (Task)

Класс для управления задачами.

### Конструктор

```python
class Task:
    def __init__(
        self,
        task_id: str,
        owner_id: str,
        task_type: TaskType,
        requirements: Dict[str, Any],
        config: Dict[str, Any],
        priority: TaskPriority = TaskPriority.NORMAL
    ):
        """
        Инициализация задачи
        
        Args:
            task_id: Уникальный идентификатор задачи
            owner_id: Идентификатор владельца
            task_type: Тип задачи
            requirements: Требования к ресурсам
            config: Конфигурация задачи
            priority: Приоритет задачи
        """
```

### Статические методы создания

```python
@staticmethod
def create_range_reduce(
    owner_id: str,
    start: int,
    end: int,
    operation: str,
    requirements: Dict[str, Any],
    config: Dict[str, Any]
) -> Task:
    """Создание задачи range_reduce"""
    
@staticmethod
def create_map(
    owner_id: str,
    data: List[Any],
    operation: str,
    requirements: Dict[str, Any],
    config: Dict[str, Any]
) -> Task:
    """Создание задачи map"""
    
@staticmethod
def create_map_reduce(
    owner_id: str,
    data: List[Any],
    map_operation: str,
    reduce_operation: str,
    requirements: Dict[str, Any],
    config: Dict[str, Any]
) -> Task:
    """Создание задачи map_reduce"""
    
@staticmethod
def create_matrix_ops(
    owner_id: str,
    matrix_a: List[List[float]],
    matrix_b: List[List[float]],
    operation: str,
    requirements: Dict[str, Any],
    config: Dict[str, Any]
) -> Task:
    """Создание задачи matrix_ops"""
    
@staticmethod
def create_ml_inference(
    owner_id: str,
    model_path: str,
    input_data: Any,
    requirements: Dict[str, Any],
    config: Dict[str, Any]
) -> Task:
    """Создание задачи ml_inference"""
    
@staticmethod
def create_ml_train_step(
    owner_id: str,
    model_path: str,
    training_data: Any,
    requirements: Dict[str, Any],
    config: Dict[str, Any]
) -> Task:
    """Создание задачи ml_train_step"""
```

### Основные методы

#### Управление задачей

```python
def to_dict(self) -> Dict[str, Any]:
    """Преобразование в словарь"""
    
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> Task:
    """Создание из словаря"""
    
def validate(self) -> List[str]:
    """Валидация задачи"""
    
def estimate_cost(self, node_reputation: float) -> float:
    """Оценка стоимости выполнения"""
```

#### Управление чанками

```python
def create_chunks(self, chunk_size: int = 100) -> List[Chunk]:
    """Создание чанков задачи"""
    
def get_chunk_requirements(self, chunk_id: str) -> Dict[str, Any]:
    """Получение требований к чанку"""
    
def aggregate_results(self, chunk_results: List[Any]) -> Any:
    """Агрегация результатов чанков"""
```

### Пример использования

```python
from src.core.task import Task, TaskType, TaskPriority

async def task_example():
    # Создание задачи range_reduce
    task = Task.create_range_reduce(
        owner_id="user-001",
        start=1,
        end=10000,
        operation="sum",
        requirements={
            "cpu_percent": 25.0,
            "ram_gb": 1.0,
            "timeout_seconds": 60,
            "max_price": 0.05
        },
        config={
            "priority": TaskPriority.NORMAL.value,
            "chunk_size": 1000
        }
    )
    
    print(f"🆔 Задача создана: {task.task_id}")
    print(f"📊 Тип: {task.task_type}")
    print(f"💰 Оценка стоимости: {task.estimate_cost(0.8):.4f}")
    
    # Валидация
    errors = task.validate()
    if errors:
        print(f"❌ Ошибки валидации: {errors}")
    else:
        print("✅ Задача валидна")
    
    # Создание чанков
    chunks = task.create_chunks(chunk_size=2000)
    print(f"🔢 Создано чанков: {len(chunks)}")
    
    # Преобразование в словарь
    task_dict = task.to_dict()
    print(f"📄 Размер словаря: {len(task_dict)} полей")
```

---

## 💰 Compute-кредиты (Credits)

Класс для управления compute-кредитами.

### Конструктор

```python
class Credits:
    def __init__(
        self,
        initial_balance: float = 100.0,
        max_balance: float = 10000.0,
        min_transfer: float = 0.1
    ):
        """
        Инициализация системы кредитов
        
        Args:
            initial_balance: Начальный баланс
            max_balance: Максимальный баланс
            min_transfer: Минимальный перевод
        """
```

### Основные методы

#### Управление балансом

```python
def get_balance(self) -> float:
    """Получение текущего баланса"""
    
def add_credits(self, amount: float, reason: str = "system") -> bool:
    """
    Добавление кредитов
    
    Args:
        amount: Количество кредитов
        reason: Причина добавления
        
    Returns:
        success: Успешность операции
    """
    
def remove_credits(self, amount: float, reason: str = "system") -> bool:
    """
    Удаление кредитов
    
    Args:
        amount: Количество кредитов
        reason: Причина удаления
        
    Returns:
        success: Успешность операции
    """
    
def transfer_credits(self, to_node: str, amount: float) -> bool:
    """
    Перевод кредитов другому узлу
    
    Args:
        to_node: Идентификатор получателя
        amount: Количество кредитов
        
    Returns:
        success: Успешность перевода
    """
```

#### История транзакций

```python
def get_transaction_history(self, limit: int = 100) -> List[CreditTransaction]:
    """
    Получение истории транзакций
    
    Args:
        limit: Лимит записей
        
    Returns:
        transactions: Список транзакций
    """
    
def get_transaction_details(self, transaction_id: str) -> Optional[CreditTransaction]:
    """
    Получение деталей транзакции
    
    Args:
        transaction_id: Идентификатор транзакции
        
    Returns:
        transaction: Детали транзакции
    """
```

#### Аналитика

```python
def get_credit_metrics(self) -> Dict[str, Any]:
    """Получение метрик кредитов"""
    
def predict_credit_flow(self, days: int = 30) -> Dict[str, Any]:
    """
    Прогнозирование кредитного потока
    
    Args:
        days: Количество дней для прогноза
        
    Returns:
        prediction: Прогноз
    """
```

### Пример использования

```python
from src.core.credits import Credits, CreditTransaction

async def credits_example():
    # Создание системы кредитов
    credits = Credits(initial_balance=500.0, max_balance=10000.0)
    
    print(f"💰 Начальный баланс: {credits.get_balance()}")
    
    # Добавление кредитов
    success = credits.add_credits(100.0, "task_reward")
    if success:
        print(f"✅ Добавлено 100 кредитов")
    
    # Перевод кредитов
    success = credits.transfer_credits("node-002", 50.0)
    if success:
        print(f"✅ Переведено 50 кредитов node-002")
    
    # Получение баланса
    balance = credits.get_balance()
    print(f"💰 Текущий баланс: {balance}")
    
    # История транзакций
    history = credits.get_transaction_history(limit=10)
    print(f"📊 История транзакций: {len(history)} записей")
    
    for tx in history:
        print(f"  - {tx.timestamp}: {tx.amount} ({tx.type})")
    
    # Метрики
    metrics = credits.get_credit_metrics()
    print(f"📈 Метрики: {metrics}")
```

---

## 🏆 Репутация (Reputation)

Класс для управления репутацией узлов.

### Конструктор

```python
class Reputation:
    def __init__(
        self,
        initial_score: float = 0.5,
        decay_rate: float = 0.01,
        reward_multiplier: float = 1.2,
        penalty_multiplier: float = 1.5
    ):
        """
        Инициализация репутационной системы
        
        Args:
            initial_score: Начальный балл
            decay_rate: Скорость затухания
            reward_multiplier: Множитель вознаграждений
            penalty_multiplier: Множитель штрафов
        """
```

### Основные методы

#### Управление репутацией

```python
def get_score(self) -> float:
    """Получение текущего балла репутации"""
    
def get_level(self) -> str:
    """Получение уровня репутации"""
    
def add_positive_feedback(self, amount: float = 1.0) -> None:
    """Добавление положительной обратной связи"""
    
def add_negative_feedback(self, amount: float = 1.0) -> None:
    """Добавление отрицательной обратной связи"""
    
def update_score(self, success: bool, quality: float = 1.0) -> None:
    """
    Обновление балла репутации
    
    Args:
        success: Успешность выполнения
        quality: Качество выполнения (0.0 - 1.0)
    """
```

#### Метрики репутации

```python
def get_metrics(self) -> Dict[str, float]:
    """Получение метрик репутации"""
    
def calculate_success_rate(self) -> float:
    """Расчет успешности выполнения"""
    
def calculate_quality_score(self) -> float:
    """Расчет оценки качества"""
    
def calculate_consistency(self) -> float:
    """Расчет последовательности"""
```

#### Аналитика

```python
def get_reputation_trend(self, days: int = 30) -> Dict[str, Any]:
    """
    Получение тренда репутации
    
    Args:
        days: Количество дней
        
    Returns:
        trend: Тренд репутации
    """
    
def predict_reputation_score(self, actions: List[Dict[str, Any]]) -> float:
    """
    Прогнозирование балла репутации
    
    Args:
        actions: Список ожидаемых действий
        
    Returns:
        predicted_score: Прогнозируемый балл
    """
```

### Пример использования

```python
from src.core.reputation import Reputation

async def reputation_example():
    # Создание репутационной системы
    reputation = Reputation(
        initial_score=0.5,
        decay_rate=0.01,
        reward_multiplier=1.2,
        penalty_multiplier=1.5
    )
    
    print(f"🏆 Начальный балл: {reputation.get_score()}")
    print(f"📊 Уровень: {reputation.get_level()}")
    
    # Успешное выполнение задачи
    reputation.update_score(success=True, quality=0.9)
    print(f"✅ После успешного выполнения: {reputation.get_score()}")
    
    # Неудачное выполнение задачи
    reputation.update_score(success=False, quality=0.3)
    print(f"❌ После неудачного выполнения: {reputation.get_score()}")
    
    # Положительная обратная связь
    reputation.add_positive_feedback(0.5)
    print(f"👍 После положительной обратной связи: {reputation.get_score()}")
    
    # Метрики
    metrics = reputation.get_metrics()
    print(f"📈 Метрики: {metrics}")
    
    # Тренд
    trend = reputation.get_reputation_trend(days=7)
    print(f"📊 Тренд за 7 дней: {trend}")
```

---

## 🔒 Sandbox слой

`src/sandbox/execution.py` предоставляет унифицированный API для изоляции пользовательского кода.

### Основные сущности

- `SandboxType` — enum (`process_isolation`, `wasm`, `container`).
- `SandboxLimits` — лимиты CPU/памяти/времени/файлов + optional env.
- `CodeBundle` — описание исполняемого пакета (entrypoint, дополнительные файлы, stdin, аргументы).
- `SandboxResult` — stdout/stderr/exit_code/runtime + флаги `timed_out`, `killed`, `usage`.
- `SandboxExecutor` — абстрактный базовый класс с методами `execute(job, code_bundle, limits)` и `run_self_test()`.
- `SandboxExecutorFactory.create()` — точка входа для получения конкретной реализации (сейчас `ProcessSandboxExecutor` + заглушки WASM/Container).

### Пример использования

```python
from sandbox.execution import (
    CodeBundle,
    SandboxExecutorFactory,
    SandboxLimits,
    SandboxType,
)

async def sandbox_example():
    executor = SandboxExecutorFactory.create(
        SandboxType.PROCESS_ISOLATION,
        SandboxLimits(cpu_time_seconds=10, memory_bytes=128 * 1024 * 1024),
    )

    bundle = CodeBundle(
        entrypoint="script.py",
        source="import json; data=json.load(open('input.json')); print(sum(data['values']))",
        files={"input.json": '{"values": [1, 2, 3, 4]}'},
    )

    result = await executor.execute(job=None, code_bundle=bundle, limits=None)
    if result.success:
        print(f"📊 STDOUT: {result.stdout.strip()}")
    else:
        print(f"❌ Ошибка: {result.stderr}")

    await executor.close()
```

`ProcessSandboxExecutor` ограничивает ресурсы через `resource.setrlimit` и автоматически удаляет временную директорию. `run_self_test()` доступен для быстрой проверки окружения и вызывается `ComputeNetwork` на старте.

---

## 💡 Примеры использования

### Пример 1: Базовое использование сети

```python
import asyncio
from src.main import ComputeNetwork
from src.core.task import Task, TaskType, TaskPriority

async def basic_example():
    # Создание сети
    network = ComputeNetwork(host="127.0.0.1", port=5557)
    
    try:
        # Запуск
        await network.start()
        await asyncio.sleep(2)
        
        print(f"🆔 Узел запущен: {network.node.node_id}")
        
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
        
        # Подача задачи
        task_id = await network.submit_task(task.to_dict())
        print(f"📝 Задача создана: {task_id}")
        
        # Мониторинг выполнения
        while True:
            status = await network.get_task_status(task_id)
            print(f"📊 Статус: {status['status']}")
            
            if status['status'] == 'completed':
                result = await network.get_task_result(task_id)
                print(f"🎉 Результат: {result}")
                break
            elif status['status'] == 'failed':
                print(f"❌ Задача не выполнена")
                break
                
            await asyncio.sleep(1)
            
    finally:
        await network.stop()

asyncio.run(basic_example())
```

### Пример 2: Пакетная обработка данных

```python
import asyncio
import numpy as np
from src.main import ComputeNetwork
from src.core.task import Task, TaskType, TaskPriority

async def batch_processing_example():
    # Создание сети
    network = ComputeNetwork(host="127.0.0.1", port=5558)
    
    try:
        # Запуск
        await network.start()
        await asyncio.sleep(2)
        
        # Генерация тестовых данных
        data = np.random.rand(10000, 100)  # 10,000 векторов по 100 элементов
        
        # Разбиение на пакеты
        batch_size = 1000
        batches = [data[i:i+batch_size] for i in range(0, len(data), batch_size)]
        
        tasks = []
        
        # Создание задач для каждого пакета
        for i, batch in enumerate(batches):
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
            print(f"📦 Задача {i+1}/{len(batches)}: {task_id}")
        
        # Ожидание завершения всех задач
        results = []
        for task_id in tasks:
            while True:
                status = await network.get_task_status(task_id)
                if status['status'] == 'completed':
                    result = await network.get_task_result(task_id)
                    results.append(result)
                    break
                await asyncio.sleep(1)
        
        # Агрегация результатов
        final_result = np.mean(results, axis=0)
        print(f"🎯 Финальный результат: {final_result}")
        
    finally:
        await network.stop()

asyncio.run(batch_processing_example())
```

### Пример 3: ML инференс

```python
import asyncio
from src.main import ComputeNetwork
from src.core.task import Task, TaskType, TaskPriority

async def ml_inference_example():
    # Создание сети
    network = ComputeNetwork(host="127.0.0.1", port=5559)
    
    try:
        # Запуск
        await network.start()
        await asyncio.sleep(2)
        
        # Путь к модели
        model_path = "models/resnet50.h5"
        
        # Тестовые данные
        input_data = {
            "image_data": "base64_encoded_image",
            "preprocessing": {
                "normalize": True,
                "resize": (224, 224)
            }
        }
        
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
                "return_probabilities": True
            }
        )
        
        # Подача задачи
        task_id = await network.submit_task(task.to_dict())
        print(f"🤖 ML задача создана: {task_id}")
        
        # Ожидание результата
        while True:
            status = await network.get_task_status(task_id)
            print(f"📊 Статус: {status['status']}")
            
            if status['status'] == 'completed':
                result = await network.get_task_result(task_id)
                print(f"🎯 Предсказание: {result['predictions']}")
                print(f"📈 Вероятности: {result['probabilities']}")
                break
            elif status['status'] == 'failed':
                print(f"❌ ML инференс не выполнен")
                break
                
            await asyncio.sleep(2)
            
    finally:
        await network.stop()

asyncio.run(ml_inference_example())
```

### Пример 4: Мониторинг и статистика

```python
import asyncio
from src.main import ComputeNetwork

async def monitoring_example():
    # Создание сети
    network = ComputeNetwork(host="127.0.0.1", port=5560)
    
    try:
        # Запуск
        await network.start()
        await asyncio.sleep(2)
        
        # Мониторинг в реальном времени
        while True:
            try:
                # Метрики сети
                network_metrics = await network.get_network_metrics()
                print(f"🌐 Узлов в сети: {network_metrics['total_nodes']}")
                print(f"📊 Активных задач: {network_metrics['active_tasks']}")
                print(f"💾 Использование CPU: {network_metrics['cpu_usage']:.1f}%")
                print(f"🧠 Использование RAM: {network_metrics['ram_usage']:.1f}%")
                
                # Метрики задач
                task_metrics = await network.get_task_metrics()
                print(f"⏱️  Среднее время выполнения: {task_metrics['avg_execution_time']:.2f}s")
                print(f"📈 Успешность: {task_metrics['success_rate']:.1f}%")
                print(f"💰 Средняя стоимость: {task_metrics['avg_cost']:.4f}")
                
                # Метрики кредитов
                credit_metrics = await network.get_credit_metrics()
                print(f"💳 Баланс: {credit_metrics['balance']:.2f}")
                print(f"📊 Транзакций: {credit_metrics['total_transactions']}")
                
                print("-" * 50)
                await asyncio.sleep(10)
                
            except KeyboardInterrupt:
                break
                
    finally:
        await network.stop()

asyncio.run(monitoring_example())
```

---

## ⚠️ Обработка ошибок

### Типы исключений

```python
# Базовые исключения
class NetworkError(Exception):
    """Ошибка сети"""
    
class TaskError(Exception):
    """Ошибка задачи"""
    
class NodeError(Exception):
    """Ошибка узла"""
    
class CreditError(Exception):
    """Ошибка кредитов"""
    
class SandboxError(Exception):
    """Ошибка sandbox"""
```

### Примеры обработки ошибок

```python
import asyncio
from src.main import ComputeNetwork
from src.core.task import Task, TaskType

async def error_handling_example():
    network = ComputeNetwork(host="127.0.0.1", port=5561)
    
    try:
        await network.start()
        
        # Попытка создать некорректную задачу
        try:
            task_data = {
                "task_type": "invalid_type",
                "owner_id": "user-001",
                "requirements": {},
                "config": {}
            }
            
            task_id = await network.submit_task(task_data)
            
        except TaskError as e:
            print(f"❌ Ошибка задачи: {e}")
            
        # Попытка получить статус несуществующей задачи
        try:
            status = await network.get_task_status("nonexistent_task_id")
            
        except TaskError as e:
            print(f"❌ Задача не найдена: {e}")
            
        # Попытка подключиться к недоступному узлу
        try:
            success = await network.connect_to_node("nonexistent_node")
            
        except NetworkError as e:
            print(f"❌ Ошибка сети: {e}")
            
        # Обработка ошибок кредитов
        try:
            # Попытка перевода недостаточных кредитов
            success = network.credits.transfer_credits("node-002", 1000.0)
            
        except CreditError as e:
            print(f"❌ Ошибка кредитов: {e}")
            
    except Exception as e:
        print(f"💥 Неожиданная ошибка: {e}")
        
    finally:
        await network.stop()

asyncio.run(error_handling_example())
```

### Логирование ошибок

```python
import logging
from src.main import ComputeNetwork

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def logging_example():
    network = ComputeNetwork(host="127.0.0.1", port=5562)
    
    try:
        await network.start()
        
        # Логирование ошибок
        try:
            # Операция, которая может вызвать ошибку
            result = await network.get_task_status("invalid_id")
            
        except Exception as e:
            logger.error(f"Ошибка при получении статуса: {e}", exc_info=True)
            logger.warning("Это предупреждение о возможной проблеме")
            logger.info("Информационное сообщение")
            
    finally:
        await network.stop()

asyncio.run(logging_example())
```

---

## 📡 WebSocket API

### Подключение к WebSocket

```python
import asyncio
import websockets
import json

async def websocket_example():
    uri = "ws://localhost:5557/ws"
    
    async with websockets.connect(uri) as websocket:
        # Подписка на обновления задач
        subscribe_message = {
            "type": "subscribe",
            "event": "task_updates"
        }
        
        await websocket.send(json.dumps(subscribe_message))
        
        # Получение обновлений
        async for message in websocket:
            data = json.loads(message)
            
            if data['type'] == 'task_update':
                task_id = data['task_id']
                status = data['status']
                print(f"📊 Обновление задачи {task_id}: {status}")
                
            elif data['type'] == 'network_update':
                metrics = data['metrics']
                print(f"🌐 Обновление сети: {metrics}")
                
            elif data['type'] == 'error':
                error = data['error']
                print(f"❌ Ошибка: {error}")

asyncio.run(websocket_example())
```

### WebSocket события

```python
# События задач
{
    "type": "task_update",
    "task_id": "task_001",
    "status": "running",
    "progress": 0.5,
    "timestamp": 1234567890.123
}

# События сети
{
    "type": "network_update",
    "metrics": {
        "total_nodes": 10,
        "active_tasks": 5,
        "cpu_usage": 45.2,
        "ram_usage": 67.8
    },
    "timestamp": 1234567890.123
}

# События узлов
{
    "type": "node_update",
    "node_id": "node_001",
    "status": "online",
    "capabilities": {
        "cpu_score": 8.0,
        "ram_gb": 16.0
    },
    "timestamp": 1234567890.123
}

# Ошибки
{
    "type": "error",
    "error": "Task execution failed",
    "details": {
        "task_id": "task_001",
        "error_code": "EXECUTION_FAILED",
        "error_message": "Memory limit exceeded"
    },
    "timestamp": 1234567890.123
}
```

---

## 🎯 Заключение

API децентрализованной P2P вычислительной сети предоставляет мощный и гибкий интерфейс для:

- ✅ **Управления сетью** - запуск, остановка, мониторинг
- ✅ **Работы с задачами** - создание, мониторинг, получение результатов
- ✅ **Управления ресурсами** - compute-кредиты, репутация
- ✅ **Безопасного выполнения** - sandbox изоляция
- ✅ **Мониторинга в реальном времени** - WebSocket API

API полностью типизирован, асинхронен и предоставляет comprehensive error handling для надежной работы.

🚀 **API готов к использованию в ваших проектах!**
