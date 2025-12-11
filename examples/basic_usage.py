#!/usr/bin/env python3
"""
Базовый пример использования децентрализованной вычислительной сети
"""

import asyncio
import json
import time
from main import ComputeNetwork
from core.task import Task, TaskType, TaskPriority

async def main():
    """Основная функция примера"""
    print("🚀 Демонстрация децентрализованной вычислительной сети")
    print("=" * 60)
    
    # Создаем сеть
    network = ComputeNetwork(host='127.0.0.1', port=5556)
    
    try:
        # Запускаем сеть
        await network.start()
        
        # Даем время на запуск
        await asyncio.sleep(2)
        
        print("\n📝 Пример 1: Простая задача range_reduce")
        # Создаем задачу range_reduce
        range_task = Task.create_range_reduce(
            owner_id=network.node.node_id,
            start=1,
            end=1000,
            operation="sum",
            requirements={
                'cpu_percent': 50.0,
                'ram_gb': 0.5,
                'timeout_seconds': 30
            },
            config={
                'max_price': 0.1,
                'priority': TaskPriority.NORMAL.value # Возвращаем .value для сериализации
            },
            privacy={
                "mode": "shard",
                "zk_verify": "basic"
            }
        )
        
        # Подаем задачу
        task_id = await network.submit_task(range_task.to_dict())
        print(f"✅ Задача создана с ID: {task_id}")
        
        # Ждем назначения
        await asyncio.sleep(3)
        
        # Проверяем статус
        status = await network.get_task_status(task_id)
        print(f"📊 Статус задачи: {status}")
        
        print("\n📝 Пример 2: ML inference задача")
        # Создаем задачу ML inference
        ml_task = Task.create_ml_inference(
            owner_id=network.node.node_id,
            model_path="models/example_model.pt",
            input_data=[[1, 2, 3], [4, 5, 6]],
            model_type="pytorch",
            requirements={
                'cpu_percent': 80.0,
                'gpu_percent': 100.0,
                'ram_gb': 2.0,
                'vram_gb': 1.0,
                'timeout_seconds': 60
            },
            config={
                'max_price': 1.0,
                'priority': TaskPriority.HIGH.value # Возвращаем .value для сериализации
            },
            privacy={
                "mode": "mask",
                "zk_verify": "strict"
            }
        )
        
        # Подаем задачу
        task_id = await network.submit_task(ml_task.to_dict())
        print(f"✅ ML задача создана с ID: {task_id}")
        
        # Ждем назначения
        await asyncio.sleep(3)
        
        # Проверяем статус
        status = await network.get_task_status(task_id)
        print(f"📊 Статус ML задачи: {status}")
        
        print("\n📝 Пример 3: Matrix operations")
        # Создаем задачу операций с матрицами
        matrix_task = Task.create_matrix_ops(
            owner_id=network.node.node_id,
            operation="multiply",
            matrix_a=[[1, 2], [3, 4]],
            matrix_b=[[5, 6], [7, 8]],
            requirements={
                'cpu_percent': 60.0,
                'ram_gb': 1.0,
                'timeout_seconds': 30
            },
            config={
                'max_price': 0.2,
                'priority': TaskPriority.NORMAL.value # Возвращаем .value для сериализации
            }
        )
        
        # Подаем задачу
        task_id = await network.submit_task(matrix_task.to_dict())
        print(f"✅ Matrix задача создана с ID: {task_id}")
        
        # Ждем назначения
        await asyncio.sleep(3)
        
        # Проверяем статус
        status = await network.get_task_status(task_id)
        print(f"📊 Статус matrix задачи: {status}")
        
        print("\n📊 Статистика сети:")
        network_status = await network.get_network_status()
        print(json.dumps(network_status, indent=2))
        
        print("\n💳 Кредитная статистика:")
        credit_stats = network.credit_manager.get_credit_statistics()
        print(json.dumps(credit_stats, indent=2))
        
        print("\n📈 Аналитика ценообразования:")
        pricing_analytics = network.pricing_engine.get_pricing_analytics()
        print(f"Рыночное условие: {pricing_analytics['market_condition']}")
        print(f"Текущие цены: {pricing_analytics['current_prices']}")
        
        print("\n🏆 Топ узлов по репутации:")
        top_nodes = await network.reputation_manager.get_top_nodes(5)
        for i, node in enumerate(top_nodes, 1):
            print(f"{i}. {node['node_id']}: {node['score']:.3f} ({node['level']})")

        print("\n📝 Пример 4: generic python_script")
        generic_task = Task.create_generic(
            owner_id=network.node.node_id,
            code_ref={
                "type": "python_script",
                "entry": "main.py",
                "source": "import json\nprint(sum(json.load(open('input.json'))['nums']))",
                "files": {"input.json": '{"nums":[1,2,3,4]}'},
            },
            input_data=None,
            requirements={
                "cpu_percent": 10.0,
                "ram_gb": 0.1,
                "timeout_seconds": 5,
            },
            config={"max_price": 0.05, "priority": TaskPriority.NORMAL.value},
            parallel={"mode": "single"},
        )
        task_id = await network.submit_task(generic_task.to_dict())
        print(f"✅ generic python_script задача создана: {task_id}")

        print("\n📝 Пример 5: pipeline с зависимостями")
        pipeline = Task.create_pipeline(
            owner_id=network.node.node_id,
            nodes=[
                {
                    "id": "step1",
                    "task": Task.create_map(
                        owner_id=network.node.node_id,
                        data=[1, 2, 3],
                        function="increment",
                        config={"priority": TaskPriority.NORMAL.value},
                        requirements={"cpu_percent": 5.0, "ram_gb": 0.1},
                    ).to_dict(),
                },
                {
                    "id": "step2",
                    "depends_on": ["step1"],
                    "task": Task.create_map_reduce(
                        owner_id=network.node.node_id,
                        data=[],  # будет подставлено из step1
                        map_function="x",
                        reduce_function="sum",
                        config={"priority": TaskPriority.NORMAL.value},
                        requirements={"cpu_percent": 5.0, "ram_gb": 0.1},
                    ).to_dict(),
                },
            ],
            config={"priority": TaskPriority.NORMAL.value},
        )
        task_id = await network.submit_task(pipeline.to_dict())
        print(f"✅ Pipeline задача создана: {task_id}")
        
        print("\n⏳ Демонстрация завершена. Нажмите Ctrl+C для выхода...")
        
        # Ждем завершения
        while True:
            await asyncio.sleep(10)
            
            # Показываем текущий статус
            active_count = len(network.active_tasks)
            pending_count = len(network.pending_tasks)
            peers_count = len(network.node.peers)
            
            print(f"\r📊 Активные задачи: {active_count} | Ожидающие: {pending_count} | Пиры: {peers_count}", end="")
            
    except KeyboardInterrupt:
        print("\n\n👋 Завершение демонстрации...")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
    finally:
        await network.stop()

if __name__ == "__main__":
    asyncio.run(main())
