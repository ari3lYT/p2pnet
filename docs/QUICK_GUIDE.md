# Краткое руководство

Это сжатая версия документации: как подготовить окружение, запустить узел и понять основные процессы за 5 минут.

## 1. Минимальные требования
- Python 3.11+
- Unix-подобная ОС (Linux/macOS) или WSL2
- Открытые порты для входящих соединений (по умолчанию TCP/UDP 5555)
- Опционально GPU с драйверами, если планируете ML задачи

## 2. Установка
```bash
git clone https://example.com/p2p-compute.git
cd p2p-compute
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Быстрый старт узла
```bash
python src/main.py --host 0.0.0.0 --port 5555 --config config/network_config.json
```
- `--debug` включит подробные логи.
- `--sandbox` (`wasm|container|process_isolation`) принудительно выбирает тип песочницы.

## 4. Как это работает в целом
1. Вы запускаете `ComputeNetwork`, он поднимает локальный `ComputeNode` и подключается к соседям.
2. Клиентский код создаёт `Task` через `Task.create_*`, сетевой планировщик рассылает его по сети.
3. Узлы-воркеры обмениваются возможностями, цены вычисляются динамически (`DynamicPricingEngine`), лучшие узлы получают назначения.
4. Кредиты владельца резервируются в `CreditManager` до завершения выполнения.
5. Результаты подписываются воркером, проверяются пирами и возвращаются инициатору.
6. Репутация и баланс обновляются автоматически.

## 5. Типовой клиентский сценарий (Python)
```python
import asyncio
from src.main import ComputeNetwork
from src.core.task import Task

async def demo():
    network = ComputeNetwork(host="127.0.0.1", port=5556)
    task = Task.create_range_reduce(
        owner_id=network.node.node_id,
        start=1, end=100000, operation="sum"
    )
    task_id = await network.submit_task(task.to_dict())
    print("Task submitted:", task_id)

asyncio.run(demo())
```

## 6. Что ещё важно
- **Безопасность:** ключи узла хранятся локально, коммуникация шифрована (см. `docs/ARCHITECTURE_OVERVIEW.md`).
- **Много клиентов:** CLI, SDK и API используют одинаковый формат сообщений, поэтому вы можете писать свои клиенты на любом языке.
- **Децентрализация:** нет центрального координирующего сервера. Вся информация реплицируется через P2P overlay и CRDT‑состояния.

## 7. Следующие шаги
- Изучите `docs/ARCHITECTURE_OVERVIEW.md`, чтобы понять слои системы.
- Настройте `config/network_config.json` (sandbox, pricing, reputation).
- Разверните несколько узлов на разных машинах и убедитесь в связности сети.
