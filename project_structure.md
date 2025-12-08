# Структура проекта децентрализованной P2P вычислительной сети

```
p2p-compute-network/
├── src/
│   ├── core/
│   │   ├── node.py           # Основной класс узла
│   │   ├── network.py        # P2P сеть и discovery
│   │   ├── task.py           # Описание задач
│   │   ├── execution.py      # Исполнение в sandbox
│   │   └── credits.py        # Compute credits
│   ├── protocol/
│   │   ├── messages.py       # Протокол коммуникации
│   │   ├── validation.py     # Валидация задач
│   │   └── security.py       # Безопасность и подписи
│   ├── tasks/
│   │   ├── range_reduce.py   # Реализация range_reduce
│   │   ├── map_reduce.py     # Реализация map_reduce
│   │   ├── matrix_ops.py     # Операции с матрицами
│   │   └── ml_ops.py         # ML операции
│   ├── sandbox/
│   │   ├── wasm_executor.py  # WASM исполнение
│   │   ├── container.py      # Container изоляция
│   │   └── resource_limits.py # Лимиты ресурсов
│   ├── reputation/
│   │   ├── system.py         # Система репутации
│   │   └── stats.py          # Статистика
│   └── pricing/
│       ├── dynamic.py        # Динамическое ценообразование
│       └── calculator.py     # Расчет стоимости
├── config/
│   ├── network_config.json   # Конфигурация сети
│   └── task_types.json       # Типы задач
├── tests/
│   ├── unit/
│   ├── integration/
│   └── benchmarks/
├── examples/
│   ├── basic_usage.py
│   └── ml_training_example.py
├── docs/
│   ├── API.md
│   ├── SECURITY.md
│   └── DEPLOYMENT.md
└── main.py                    # Точка входа