
# 🚀 Продвинутые примеры задач и развертывания

## 📋 Содержание

1. [Продвинутые примеры задач](#продвинутые-примеры-задач)
2. [Масштабные развертывания](#масштабные-развертывания)
3. [Оптимизация производительности](#оптимизация-производительности)
4. [Интеграция с внешними системами](#интеграция-с-внешними-системами)
5. [Кастомизация и расширение](#кастомизация-и-расширение)
6. [Мониторинг и аналитика](#мониторинг-и-аналитика)
7. [Тестирование и валидация](#тестирование-и-валидация)

---

## 🎯 Продвинутые примеры задач

### Пример 1: Обработка больших данных с MapReduce

```python
import asyncio
import sys
import os
import json
import random
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import ComputeNetwork
from core.task import Task, TaskType, TaskPriority

async def big_data_processing():
    """Обработка больших данных с использованием MapReduce"""
    
    print("📊 Обработка больших данных с MapReduce")
    
    network = ComputeNetwork(host='127.0.0.1', port=5563)
    
    try:
        await network.start()
        await asyncio.sleep(2)
        
        # Генерируем большой набор данных (1M записей)
        print("📦 Генерация тестовых данных...")
        large_dataset = []
        for i in range(1000000):
            record = {
                'id': i,
                'value': random.uniform(0, 100),
                'category': random.choice(['A', 'B', 'C', 'D']),
                'timestamp': time.time() - random.randint(0, 86400)  # За последние 24 часа
            }
            large_dataset.append(record)
        
        print(f"✅ Сгенерировано {len(large_dataset)} записей")
        
        # Задача 1: Агрегация по категориям
        category_task = Task.create_map_reduce(
            owner_id=network.node.node_id,
            data=large_dataset,
            map_function="record['category']",
            reduce_function="count_by_category",
            requirements={
                'cpu_percent': 60.0,
                'ram_gb': 4.0,
                'timeout_seconds': 600
            },
            config={
                'max_price': 5.0,
                'priority': TaskPriority.HIGH.value
            }
        )
        
        task_id1 = await network.submit_task(category_task.to_dict())
        print(f"✅ Задача агрегации по категориям создана: {task_id1}")
        
        # Задача 2: Расчет статистики по значениям
        stats_task = Task.create_map_reduce(
            owner_id=network.node.node_id,
            data=large_dataset,
            map_function="record['value']",
            reduce_function="calculate_statistics",
            requirements={
                'cpu_percent': 50.0,
                'ram_gb': 3.0,
                'timeout_seconds': 300
            },
            config={
                'max_price': 3.0,
                'priority': TaskPriority.NORMAL.value
            }
        )
        
        task_id2 = await network.submit_task(stats_task.to_dict())
        print(f"✅ Задача расчета статистики создана: {task_id2}")
        
        # Задача 3: Фильтрация и группировка по времени
        time_task = Task.create_map_reduce(
            owner_id=network.node.node_id,
            data=large_dataset,
            map_function="record['timestamp']",
            reduce_function="group_by_hour",
            requirements={
                'cpu_percent': 40.0,
                'ram_gb': 2.0,
                'timeout_seconds': 240
            },
            config={
                'max_price': 2.0,
                'priority': TaskPriority.NORMAL.value
            }
        )
        
        task_id3 = await network.submit_task(time_task.to_dict())
        print(f"✅ Задача группировки по времени создана: {task_id3}")
        
        # Мониторинг прогресса
        start_time = time.time()
        completed = 0
        
        while completed < 3:
            await asyncio.sleep(10)
            
            completed = 0
            for task_id in [task_id1, task_id2, task_id3]:
                status = await network.get_task_status(task_id)
                if status['status'] == 'completed':
                    completed += 1
                    print(f"✅ Задача {task_id} завершена")
            
            elapsed = time.time() - start_time
            print(f"📊 Прогресс: {completed}/3 задач завершено за {elapsed:.1f}s")
        
        # Сбор результатов
        results = {}
        for task_id in [task_id1, task_id2, task_id3]:
            status = await network.get_task_status(task_id)
            if status['status'] == 'completed':
                results[task_id] = status.get('result', {})
        
        print(f"🎉 Обработка завершена! Результаты:")
        for task_id, result in results.items():
            print(f"  Задача {task_id}: {result}")
        
        # Сохранение результатов
        with open('big_data_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
    finally:
        await network.stop()

# Запуск
asyncio.run(big_data_processing())
```

### Пример 2: Комплексный ML пайплайн

```python
import asyncio
import sys
import os
import numpy as np
import json
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import ComputeNetwork
from core.task import Task, TaskType, TaskPriority

async def ml_pipeline():
    """Комплексный ML пайплайн с несколькими этапами"""
    
    print("🤖 Комплексный ML пайплайн")
    
    network = ComputeNetwork(host='127.0.0.1', port=5564)
    
    try:
        await network.start()
        await asyncio.sleep(2)
        
        # Этап 1: Генерация синтетических данных
        print("📊 Генерация обучающих данных...")
        
        def generate_synthetic_data():
            """Генерация синтетических данных для классификации"""
            data = []
            for i in range(10000):
                # Генерация признаков
                x1 = np.random.normal(0, 1)
                x2 = np.random.normal(0, 1)
                
                # Генерация метки (класс 0 или 1)
                if x1 + x2 > 0:
                    label = 1
                else:
                    label = 0
                
                data.append([x1, x2, label])
            
            return data
        
        # Создаем задачу генерации данных
        data_task = Task.create_map(
            owner_id=network.node.node_id,
            data=list(range(10000)),
            function="generate_synthetic_data",
            requirements={
                'cpu_percent': 30.0,
                'ram_gb': 2.0
            },
            config={
                'max_price': 1.0,
                'priority': TaskPriority.NORMAL.value
            }
        )
        
        data_task_id = await network.submit_task(data_task.to_dict())
        print(f"✅ Задача генерации данных создана: {data_task_id}")
        
        # Ждем завершения генерации данных
        while True:
            status = await network.get_task_status(data_task_id)
            if status['status'] == 'completed':
                synthetic_data = status.get('result', {}).get('data', [])
                break
            await asyncio.sleep(2)
        
        print(f"✅ Сгенерировано {len(synthetic_data)} примеров данных")
        
        # Этап 2: Разделение данных на train/test
        print("🔀 Разделение данных на train/test...")
        
        split_task = Task.create_map_reduce(
            owner_id=network.node.node_id,
            data=synthetic_data,
            map_function="split_data",
            reduce_function="combine_splits",
            requirements={
                'cpu_percent': 20.0,
                'ram_gb': 1.0
            },
            config={
                'max_price': 0.5,
                'priority': TaskPriority.LOW.value
            }
        )
        
        split_task_id = await network.submit_task(split_task.to_dict())
        
        # Этап 3: Обучение модели
        print("🎓 Обучение модели...")
        
        train_task = Task.create_ml_train_step(
            owner_id=network.node.node_id,
            model_path="models/logistic_regression.pkl",
            train_data=synthetic_data[:8000],  # 80% для обучения
            model_type="sklearn",
            requirements={
                'cpu_percent': 70.0,
                'ram_gb': 3.0,
                'gpu_percent': 0.0
            },
            config={
                'max_price': 3.0,
                'priority': TaskPriority.HIGH.value
            }
        )
        
        train_task_id = await network.submit_task(train_task.to_dict())
        print(f"✅ Задача обучения создана: {train_task_id}")
        
        # Этап 4: Оценка модели
        print("📈 Оценка модели...")
        
        test_data = synthetic_data[8000:]  # 20% для теста
        
        eval_task = Task.create_ml_inference(
            owner_id=network.node.node_id,
            model_path="models/logistic_regression.pkl",
            input_data=test_data,
            model_type="sklearn",
            requirements={
                'cpu_percent': 40.0,
                'ram_gb': 2.0
            },
            config={
                'max_price': 1.0,
                'priority': TaskPriority.NORMAL.value
            }
        )
        
        eval_task_id = await network.submit_task(eval_task.to_dict())
        print(f"✅ Задача оценки создана: {eval_task_id}")
        
        # Этап 5: Визуализация результатов
        print("📊 Визуализация результатов...")
        
        def visualize_results(predictions, true_labels):
            """Визуализация результатов"""
            import matplotlib.pyplot as plt
            
            # Создание визуализации
            plt.figure(figsize=(10, 6))
            
            # ROC кривая
            fpr, tpr, _ = roc_curve(true_labels, predictions)
            auc_score = auc(fpr, tpr)
            
            plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {auc_score:.2f})')
            plt.plot([0, 1], [0, 1], 'k--')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('ROC Curve')
            plt.legend()
            
            # Сохранение
            plt.savefig('roc_curve.png')
            plt.close()
            
            return {
                'auc_score': auc_score,
                'fpr': fpr.tolist(),
                'tpr': tpr.tolist()
            }
        
        vis_task = Task.create_map(
            owner_id=network.node.node_id,
            data=[predictions, true_labels],
            function="visualize_results",
            requirements={
                'cpu_percent': 30.0,
                'ram_gb': 1.0
            },
            config={
                'max_price': 0.5,
                'priority': TaskPriority.LOW.value
            }
        )
        
        vis_task_id = await network.submit_task(vis_task.to_dict())
        print(f"✅ Задача визуализации создана: {vis_task_id}")
        
        # Мониторинг всего пайплайна
        pipeline_tasks = [data_task_id, split_task_id, train_task_id, eval_task_id, vis_task_id]
        completed = 0
        
        while completed < len(pipeline_tasks):
            await asyncio.sleep(5)
            
            completed = 0
            for task_id in pipeline_tasks:
                status = await network.get_task_status(task_id)
                if status['status'] == 'completed':
                    completed += 1
                    print(f"✅ Этап {pipeline_tasks.index(task_id) + 1} завершен")
        
        # Сбор результатов всего пайплайна
        pipeline_results = {}
        for task_id in pipeline_tasks:
            status = await network.get_task_status(task_id)
            if status['status'] == 'completed':
                stage_name = ['data_generation', 'data_split', 'training', 'evaluation', 'visualization'][pipeline_tasks.index(task_id)]
                pipeline_results[stage_name] = status.get('result', {})
        
        # Сохранение результатов пайплайна
        with open('ml_pipeline_results.json', 'w') as f:
            json.dump(pipeline_results, f, indent=2)
        
        print(f"🎉 ML пайплайн завершен! Результаты:")
        for stage, result in pipeline_results.items():
            print(f"  {stage}: {result}")
        
        # Вывод итоговой метрики
        if 'evaluation' in pipeline_results:
            auc_score = pipeline_results['evaluation'].get('auc_score', 0)
            print(f"📊 Итоговая метрика AUC: {auc_score:.3f}")
        
    finally:
        await network.stop()

# Запуск
asyncio.run(ml_pipeline())
```

### Пример 3: Потоковая обработка данных

```python
import asyncio
import sys
import os
import time
import json
import random
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import ComputeNetwork
from core.task import Task, TaskType, TaskPriority

class StreamProcessor:
    """Потоковый обработчик данных"""
    
    def __init__(self, network: ComputeNetwork):
        self.network = network
        self.data_stream = []
        self.processing_tasks = []
        self.results = []
    
    async def generate_data_stream(self, duration_minutes=5):
        """Генерация потока данных"""
        print("🔄 Генерация потока данных...")
        
        start_time = time.time()
        end_time = start_time + duration_minutes * 60
        
        while time.time() < end_time:
            # Генерация пакета данных
            batch_size = random.randint(10, 50)
            batch = []
            
            for i in range(batch_size):
                data_point = {
                    'id': len(self.data_stream) + i,
                    'timestamp': time.time(),
                    'value': random.uniform(0, 100),
                    'category': random.choice(['A', 'B', 'C']),
                    'quality': random.choice(['high', 'medium', 'low'])
                }
                batch.append(data_point)
            
            self.data_stream.extend(batch)
            
            # Обработка пакета
            await self.process_batch(batch)
            
            # Небольшая задержка
            await asyncio.sleep(random.uniform(0.1, 0.5))
        
        print(f"✅ Сгенерировано {len(self.data_stream)} записей")
    
    async def process_batch(self, batch):
        """Обработка пакета данных"""
        
        # Задача 1: Агрегация по категориям
        agg_task = Task.create_map_reduce(
            owner_id=self.network.node.node_id,
            data=batch,
            map_function="record['category']",
            reduce_function="aggregate_by_category",
            requirements={
                'cpu_percent': 30.0,
                'ram_gb': 1.0
            },
            config={
                'max_price': 0.5,
                'priority': TaskPriority.NORMAL.value
            }
        )
        
        agg_task_id = await self.network.submit_task(agg_task.to_dict())
        
        # Задача 2: Фильтрация по качеству
        filter_task = Task.create_map(
            owner_id=self.network.node.node_id,
            data=batch,
            function="filter_by_quality",
            requirements={
                'cpu_percent': 20.0,
                'ram_gb': 0.5
            },
            config={
                'max_price': 0.2,
                'priority': TaskPriority.LOW.value
            }
        )
        
        filter_task_id = await self.network.submit_task(filter_task.to_dict())
        
        # Задача 3: Расчет статистики
        stats_task = Task.create_map_reduce(
            owner_id=self.network.node.node_id,
            data=batch,
            map_function="record['value']",
            reduce_function="calculate_statistics",
            requirements={
                'cpu_percent': 25.0,
                'ram_gb': 0.8
            },
            config={
                'max_price': 0.3,
                'priority': TaskPriority.NORMAL.value
            }
        )
        
        stats_task_id = await self.network.submit_task(stats_task.to_dict())
        
        # Сохранение ID задач
        self.processing_tasks.extend([
            (agg_task_id, 'aggregation'),
            (filter_task_id, 'filter'),
            (stats_task_id, 'statistics')
        ])
    
    async def monitor_progress(self):
        """Мониторинг прогресса обработки"""
        
        print("📊 Мониторинг прогресса...")
        
        processed_count = 0
        total_tasks = len(self.processing_tasks)
        
        while processed_count < total_tasks:
            await asyncio.sleep(2)
            
            completed = 0
            for task_id, task_type in self.processing_tasks:
                status = await self.network.get_task_status(task_id)
                if status['status'] == 'completed':
                    completed += 1
                    self.results.append({
                        'task_id': task_id,
                        'type': task_type,
                        'result': status.get('result', {}),
                        'timestamp': time.time()
                    })
                    print(f"✅ {task_type} задача {task_id} завершена")
            
            processed_count = completed
            progress = (processed_count / total_tasks) * 100
            
            print(f"📈 Прогресс: {processed_count}/{total_tasks} ({progress:.1f}%)")
        
        print("🎉 Вся обработка завершена!")
    
    async def generate_report(self):
        """Генерация отчета"""
        
        print("📄 Генерация отчета...")
        
        # Агрегация результатов
        report = {
            'total_records': len(self.data_stream),
            'processing_time': time.time() - self.results[0]['timestamp'] if self.results else 0,
            'tasks_completed': len(self.results),
            'results_by_type': {},
            'summary_statistics': {}
        }
        
        # Группировка по типам задач
        for result in self.results:
            task_type = result['type']
            if task_type not in report['results_by_type']:
                report['results_by_type'][task_type] = []
            report['results_by_type'][task_type].append(result['result'])
        
        # Расчет сводной статистики
        if 'statistics' in report['results_by_type']:
            all_stats = []
            for stat_result in report['results_by_type']['statistics']:
                if isinstance(stat_result, dict):
                    all_stats.extend([
                        stat_result.get('mean', 0),
                        stat_result.get('median', 0),
                        stat_result.get('std', 0)
                    ])
            
            if all_stats:
                report['summary_statistics'] = {
                    'mean_value': sum(all_stats) / len(all_stats),
                    'total_values': len(all_stats)
                }
        
        # Сохранение отчета
        with open('stream_processing_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Отчет сгенерирован: stream_processing_report.json")
        print(f"📈 Обработано записей: {report['total_records']}")
        print(f"✅ Выполнено задач: {report['tasks_completed']}")
        print(f"⏱️ Время обработки: {report['processing_time']:.2f}с")
        
        return report

async def stream_processing_example():
    """Пример потоковой обработки"""
    
    print("🌊 Потоковая обработка данных")
    
    network = ComputeNetwork(host='127.0.0.1', port=5565)
    
    try:
        await network.start()
        await asyncio.sleep(2)
        
        # Создаем потоковый обработчик
        processor = StreamProcessor(network)
        
        # Запускаем генерацию данных и обработку параллельно
        generate_task = asyncio.create_task(processor.generate_data_stream(duration_minutes=2))
        monitor_task = asyncio.create_task(processor.monitor_progress())
        
        # Ждем завершения
        await generate_task
        await monitor_task
        
        # Генерируем отчет
        report = await processor.generate_report()
        
        return report
        
    finally:
        await network.stop()

# Запуск
asyncio.run(stream_processing_example())
```

### Пример 4: Параллельная обработка изображений

```python
import asyncio
import sys
import os
import time
import json
import random
from PIL import Image
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import ComputeNetwork
from core.task import Task, TaskType, TaskPriority

async def image_processing_pipeline():
    """Параллельная обработка изображений"""
    
    print("🖼️ Параллельная обработка изображений")
    
    network = ComputeNetwork(host='127.0.0.1', port=5566)
    
    try:
        await network.start()
        await asyncio.sleep(2)
        
        # Этап 1: Генерация тестовых изображений
        print("📸 Генерация тестовых изображений...")
        
        def generate_test_images(count=10):
            """Генерация тестовых изображений"""
            images = []
            
            for i in range(count):
                # Создание случайного изображения
                width = random.randint(256, 512)
                height = random.randint(256, 512)
                
                # Генерация случайного изображения
                img_array = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
                img = Image.fromarray(img_array)
                
                # Сохранение
                filename = f"test_image_{i}.png"
                img.save(filename)
                
                images.append({
                    'filename': filename,
                    'size': f"{width}x{height}",
                    'format': 'PNG'
                })
            
            return images
        
        # Создаем задачу генерации изображений
        generate_task = Task.create_map(
            owner_id=network.node.node_id,
            data=list(range(10)),
            function="generate_test_images",
            requirements={
                'cpu_percent': 40.0,
                'ram_gb': 2.0
            },
            config={
                'max_price': 2.0,
                'priority': TaskPriority.NORMAL.value
            }
        )
        
        generate_task_id = await network.submit_task(generate_task.to_dict())
        print(f"✅ Задача генерации изображений создана: {generate_task_id}")
        
        # Этап 2: Параллельная обработка изображений
        print("🔄 Параллельная обработка изображений...")
        
        processing_tasks = []
        
        for i in range(10):
            # Задача обработки изображения
            process_task = Task.create_matrix_ops(
                owner_id=network.node.node_id,
                matrix1=[[i, i+1], [i+2, i+3]],  # Имитация изображения
                operation="apply_filter",
                requirements={
                    'cpu_percent': 60.0,
                    'ram_gb': 1.0,
                    'gpu_percent': 50.0
                },
                config={
                    'max_price': 1.0,
                    'priority': TaskPriority.HIGH.value
                }
            )
            
            task_id = await network.submit_task(process_task.to_dict())
            processing_tasks.append((task_id, f"image_{i}"))
            print(f"✅ Задача обработки изображения {i} создана: {task_id}")
        
        # Этап 3: Агрегация результатов
        print("📊 Агрегация результатов...")
        
        aggregate_task = Task.create_map_reduce(
            owner_id=network.node.node_id,
            data=[result for _, result in processing_tasks],
            map_function="extract_features",
            reduce_function="combine_features",
            requirements={
                'cpu_percent': 30.0,
                'ram_gb': 1.0
            },
            config={
                'max_price': 1.0,
                'priority': TaskPriority.NORMAL.value
            }
        )
        
        aggregate_task_id = await network.submit_task(aggregate_task.to_dict())
        print(f"✅ Задача агрегации создана: {aggregate_task_id}")
        
        # Мониторинг прогресса
        all_tasks = [generate_task_id] + [task_id for task_id, _ in processing_tasks] + [aggregate_task_id]
        completed = 0
        
        while completed < len(all_tasks):
            await asyncio.sleep(3)
            
            completed = 0
            for task_id in all_tasks:
                status = await network.get_task_status(task_id)
                if status['status'] == 'completed':
                    completed += 1
                    task_name = {
                        generate_task_id: "Генерация изображений",
                        aggregate_task_id: "Агрегация"
                    }.get(task_id, f"Обработка изображения")
                    
                    print(f"✅ {task_name} завершена")
        
        # Сбор результатов
        results = {}
        for task_id in all_tasks:
            status = await network.get_task_status(task_id)
            if status['status'] == 'completed':
                results[task_id] = status.get('result', {})
        
        # Этап 4: Создание коллажа
        print("🎨 Создание коллажа...")
        
        collage_task = Task.create_matrix_ops(
            owner_id=network.node.node_id,
            matrix1=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],  # Имитация коллажа
            operation="create_collage",
            requirements={
                'cpu_percent': 50.0,
                'ram_gb': 2.0
            },
            config={
                'max_price': 1.5,
                'priority': TaskPriority.NORMAL.value
            }
        )
        
        collage_task_id = await network.submit_task(collage_task.to_dict())
        
        # Ожидание завершения коллажа
        while True:
            status = await network.get_task_status(collage_task_id)
            if status['status'] == 'completed':
                break
            await asyncio.sleep(2)
        
        # Финальный отчет
        print("📄 Создание финального отчета...")
        
        final_report = {
            'total_images': 10,
            'processing_time': time.time() - start_time,
            'tasks_completed': len(all_tasks),
            'results': results,
            'collage_created': True,
            'timestamp': time.time()
        }
        
        # Сохранение отчета
        with open('image_processing_report.json', 'w') as f:
            json.dump(final_report, f, indent=2)
        
        print(f"🎉 Обработка изображений завершена!")
        print(f"📊 Отчет: image_processing_report.json")
        
        return final_report
        
    finally:
        await network.stop()

# Запуск
asyncio.run(image_processing_pipeline())
```

---

## 🚀 Масштабные развертывания

### Docker Compose развертывание

#### 1. Создание docker-compose.yml

```yaml
version: '3.8'

services:
  # Сервис для сети
  compute-network:
    build: .
    ports:
      - "5555:5555"
      - "5556:5556"
      - "5557:5557"
    environment:
      - NODE_ID=node1
      - PORT=5555
      - DEBUG=true
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
    networks:
      - compute-net
    restart: unless-stopped

  # Второй узел
  compute-network-2:
    build: .
    ports:
      - "5558:5555"
    environment:
      - NODE_ID=node2
      - PORT=5555
      - DEBUG=true
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
    networks:
      - compute-net
    restart: unless-stopped
    depends_on:
      - compute-network

  # Третий узел
  compute-network-3:
    build: .
    ports:
      - "5559:5555"
    environment:
      - NODE_ID=node3
      - PORT=5555
      - DEBUG=true
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
    networks:
      - compute-net
    restart: unless-stopped
    depends_on:
      - compute-network

  # Мониторинг
  monitoring:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - compute-net

  # Визуализация метрик
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - ./monitoring/grafana:/etc/grafana/provisioning
    networks:
      - compute-net

networks:
  compute-net:
    driver: bridge

volumes:
  config:
  logs:
```

#### 2. Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY src/ ./src/
COPY config/ ./config/
COPY examples/ ./examples/

# Создание директорий
RUN mkdir -p /app/logs /app/data

# Открываем порты
EXPOSE 5555

# Переменные окружения
ENV PYTHONPATH=/app/src
ENV NODE_ID=node1
ENV PORT=5555
ENV DEBUG=false

# Запуск приложения
CMD ["python", "src/main.py", "--host", "0.0.0.0", "--port", "5555"]
```

#### 3. Конфигурация Prometheus

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'compute-network'
    static_configs:
      - targets: ['compute-network:5555', 'compute-network-2:5555', 'compute-network-3:5555']
    metrics_path: /metrics
    scrape_interval: 10s
```

#### 4. Запуск и управление

```bash
# Сборка и запуск
docker-compose up -d

# Просмотр статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f compute-network

# Масштабирование
docker-compose up -d --scale compute-network=5

# Остановка
docker-compose down

# Обновление
docker-compose pull
docker-compose up -d --force-recreate
```

### Kubernetes развертывание

#### 1. Helm Chart

```yaml
# charts/compute-network/values.yaml
replicaCount: 3

image:
  repository: compute-network
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: LoadBalancer
  port: 80
  targetPort: 5555

resources:
  limits:
    cpu: 1
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi

config:
  nodeType: "worker"
  maxPeers: 100
  debug: false

monitoring:
  enabled: true
  prometheusPort: 9090
```

#### 2. Deployment manifest

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: compute-network
  labels:
    app: compute-network
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
        - containerPort: 5555
        env:
        - name: NODE_ID
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        volumeMounts:
        - name: config
          mountPath: /app/config
        - name: logs
          mountPath: /app/logs
      volumes:
      - name: config
        configMap:
          name: compute-network-config
      - name: logs
        emptyDir: {}
```

#### 3. Service manifest

```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: compute-network-service
spec:
  selector:
    app: compute-network
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5555
  type: LoadBalancer
```

#### 4. ConfigMap

```yaml
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: compute-network-config
data:
  network.json: |
    {
      "discovery_interval": 30,
      "max_peers": 100,
      "timeout": 60,
      "retry_attempts": 3
    }
  pricing.json: |
    {
      "base_cpu_price": 0.01,
      "base_gpu_price": 0.05,
      "urgency_multiplier": {
        "low": 0.8,
        "normal": 1.0,
        "high": 1.5
      }
    }
```

#### 5. Управление кластером

```bash
# Применение конфигураций
kubectl apply -f k8s/

# Просмотр статуса
kubectl get pods
kubectl get services
kubectl get deployments

# Масштабирование
kubectl scale deployment compute-network --replicas=5

# Обновление
kubectl set image deployment/compute-network compute-network=compute-network:v2.0

# Мониторинг
kubectl logs -f deployment/compute-network
kubectl top pods

# Остановка
kubectl delete -f k8s/
```

### Облачное развертывание на AWS

#### 1. Terraform конфигурация

```hcl
# main.tf
provider "aws" {
  region = "us-east-1"
}

# VPC
resource "aws_vpc" "compute_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  
  tags = {
    Name = "compute-network-vpc"
  }
}

# Subnets
resource "aws_subnet" "compute_subnet" {
  vpc_id                  = aws_vpc.compute_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  
  tags = {
    Name = "compute-network-subnet"
  }
}

# Security Group
resource "aws_security_group" "compute_sg" {
  vpc_id = aws_vpc.compute_vpc.id
  
  ingress {
    from_port   = 5555
    to_port     = 5555
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "compute-network-sg"
  }
}

# Auto Scaling Group
resource "aws_launch_configuration" "compute_lc" {
  name_prefix   = "compute-node-"
  image_id      = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.medium"
  key_name      = "compute-key"
  
  security_groups = [aws_security_group.compute_sg.id]
  
  user_data = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y python3 python3-pip
    pip3 install -r /tmp/requirements.txt
    
    # Запуск compute node
    python3 /tmp/src/main.py --host 0.0.0.0 --port 5555 --debug
  EOF
  
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "compute_asg" {
  desired_capacity    = 3
  max_size           = 10
  min_size           = 2
  vpc_zone_identifier = [aws_subnet.compute_subnet.id]
  
  launch_configuration = aws_launch_configuration.compute_lc.name
  
  tag {
    key                 = "Name"
    value               = "compute-node"
    propagate_at_launch = true
  }
}

# Load Balancer
resource "aws_elb" "compute_elb" {
  name               = "compute-network-elb"
  availability_zones = ["us-east-1a"]
  
  listener {
    instance_port     = 5555
    instance_protocol = "tcp"
    lb_port           = 80
    lb_protocol       = "tcp"
  }
  
  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 3
    target              = "TCP:5555"
    interval            = 30
  }
  
  instances = aws_autoscaling_group.compute_asg.ids
  
  cross_zone_load_balancing   = true
  connection_draining         = true
  connection_draining_timeout = 400
  
  tags = {
    Name = "compute-network-elb"
  }
}
```

#### 2. Ansible playbook

```yaml
# ansible/playbook.yml
---
- name: Deploy Compute Network
  hosts: compute_nodes
  become: yes
  
  vars:
    python_version: "3.9"
    node_port: 5555
    debug_mode: true
  
  tasks:
    - name: Install Python dependencies
      apt:
        name: "{{ item }}"
        state: present
      loop:
        - python3
        - python3-pip
        - build-essential
    
    - name: Create application directory
      file:
        path: /opt/compute-network
        state: directory
        mode: '0755'
    
    - name: Copy application files
      copy:
        src: "{{ playbook_dir }}/"
        dest: /opt/compute-network/
        mode: '0644'
    
    - name: Install Python packages
      pip:
        requirements: /opt/compute-network/requirements.txt
        virtualenv: /opt/compute-network/venv
    
    - name: Create systemd service
      template:
        src: templates/compute-network.service.j2
        dest: /etc/systemd/system/compute-network.service
        mode: '0644'
    
    - name: Enable and start service
      systemd:
        name: compute-network
        state: started
        enabled: yes
        daemon_reload: yes
    
    - name: Configure firewall
      ufw:
        rule: allow
        port: "{{ node_port }}"
        proto: tcp
```

---

## ⚡ Оптимизация производительности

### Кластерная оптимизация

#### 1. Автоматическая балансировка нагрузки

```python
import asyncio
import time
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class LoadBalancer:
    """Балансировщик нагрузки для кластера"""
    
    def __init__(self, network):
        self.network = network
        self.node_loads: Dict[str, float] = {}
        self.task_queue = asyncio.Queue()
        self.running = False
    
    async def start(self):
        """Запуск балансировщика"""
        self.running = True
        
        # Запускаем задачи
        asyncio.create_task(self.monitor_load())
        asyncio.create_task(self.distribute_tasks())
        
        print("🔄 Балансировщик нагрузки запущен")
    
    async def stop(self):
        """Остановка балансировщика"""
        self.running = False
    
    async def monitor_load(self):
        """Мониторинг нагрузки на узлы"""
        while self.running:
            try:
                # Получаем статус сети
                status = await self.network.get_network_status()
                
                # Обновляем нагрузку на узлах
                for peer_id in self.network.node.peers:
                    # Имитация сбора метрик
                    load = await self.get_node_load(peer_id)
                    self.node_loads[peer_id] = load
                
                # Вывод текущей нагрузки
                print(f"📊 Текущая нагрузка: {self.node_loads}")
                
                await asyncio.sleep(10)  # Мониторинг каждые 10 секунд
                
            except Exception as e:
                print(f"❌ Ошибка мониторинга нагрузки: {e}")
                await asyncio.sleep(30)
    
    async def get_node_load(self, node_id: str) -> float:
        """Получение нагрузки на узле"""
        try:
            # Здесь можно реализовать реальный сбор метрик
            # Например, через API узла или мониторинговую систему
            
            # Имитация: случайная нагрузка
            import random
            return random.uniform(0.1, 0.9)
            
        except Exception as e:
            print(f"❌ Ошибка получения нагрузки узла {node_id}: {e}")
            return 1.0  # Максимальная нагрузка при ошибке
    
    async def distribute_tasks(self):
        """Распределение задач по узлам"""
        while self.running:
            try:
                # Получаем задачу из очереди
                task_data = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
                
                # Находим оптимальный узел
                optimal_node = self.find_optimal_node(task_data)
                
                if optimal_node:
                    # Назначаем задачу
                    await self.assign_task(optimal_node, task_data)
                else:
                    # Задачу нельзя выполнить
                    print(f"❌ Нет доступных узлов для задачи {task_data.get('task_id')}")
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"❌ Ошибка распределения задач: {e}")
    
    def find_optimal_node(self, task_data: Dict) -> str:
        """Находит оптимальный узел для задачи"""
        # Фильтруем доступные узлы
        available_nodes = [
            node_id for node_id, load in self.node_loads.items()
            if load < 0.8  # Нагрузка менее 80%
        ]
        
        if not available_nodes:
            return None
        
        # Выбираем узел с минимальной нагрузкой
        optimal_node = min(available_nodes, key=lambda x: self.node_loads[x])
        
        return optimal_node
    
    async def assign_task(self, node_id: str, task_data: Dict):
        """Назначение задачи узлу"""
        try:
            # Здесь должна быть логика назначения задачи
            print(f"📝 Задача {task_data.get('task_id')} назначена узлу {node_id}")
            
            # Обновляем нагрузку
            self.node_loads[node_id] += 0.1
            
        except Exception as e:
            print(f"❌ Ошибка назначения задачи: {e}")
    
    async def submit_task(self, task_data: Dict):
        """Подача задачи в балансировщик"""
        await self.task_queue.put(task_data)
        print(f"📤 Задача {task_data.get('task_id')} добавлена в очередь")
```

#### 2. Кэширование результатов

```python
import asyncio
import time
import hashlib
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class CacheEntry:
    """Запись в кэше"""
    data: Any
    timestamp: float
    ttl: float
    access_count: int = 0
    
    def is_expired(self) -> bool:
        """Проверка истечения срока действия"""
        return time.time() - self.timestamp > self.ttl
    
    def touch(self):
        """Обновление времени доступа"""
        self.access_count += 1
        self.timestamp = time.time()

class TaskCache:
    """Кэш для результатов задач"""
    
    def __init__(self, max_size: int = 1000, default_ttl: float = 3600):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: Dict[str, CacheEntry] = {}
        self.access_times: Dict[str, float] = {}
    
    def _generate_key(self, task_data: Dict) -> str:
        """Генерация ключа для задачи"""
        # Создаем уникальный ключ на основе параметров задачи
        key_data = {
            'task_type': task_data.get('task_type'),
            'parameters': task_data.get('parameters', {}),
            'requirements': task_data.get('requirements', {})
        }
        
        key_str = str(key_data)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _evict_expired(self):
        """Удаление устаревших записей"""
        current_time = time.time()
        
        # Удаляем просроченные записи
        expired_keys = [
            key for key, entry in self.cache.items()
            if entry.is_expired()
        ]
        
        for key in expired_keys:
            del self.cache[key]
            print(f"🗑️ Удалена просроченная запись: {key}")
    
    def _evict_lru(self):
        """Удаление наименее используемых записей"""
        if len(self.cache) <= self.max_size:
            return
        
        # Находим наименее используемые записи
        sorted_keys = sorted(
            self.cache.keys(),
            key=lambda k: self.access_times.get(k, 0)
        )
        
        # Удаляем самые старые записи
        keys_to_remove = sorted_keys[:len(self.cache) - self.max_size]
        
        for key in keys_to_remove:
            del self.cache[key]
            print(f"🗑️ Удалена LRU запись: {key}")
    
    async def get(self, task_data: Dict) -> Optional[Any]:
        """Получение результата из кэша"""
        key = self._generate_key(task_data)
        
        if key in self.cache:
            entry = self.cache[key]
            
            if entry.is_expired():
                del self.cache[key]
                return None
            
            entry.touch()
            self.access_times[key] = time.time()
            
            print(f"🎯 Хит кэша для задачи: {key}")
            return entry.data
        
        return None
    
    async def set(self, task_data: Dict, result: Any, ttl: Optional[float] = None):
        """Сохранение результата в кэш"""
        key = self._generate_key(task_data)
        
        # Определяем TTL
        if ttl is None:
            ttl = self.default_ttl
        
        # Создаем запись
        entry = CacheEntry(
            data=result,
            timestamp=time.time(),
            ttl=ttl
        )
        
        # Проверяем размер кэша
        if len(self.cache) >= self.max_size:
            self._evict_expired()
            self._evict_lru()
        
        # Сохраняем запись
        self.cache[key] = entry
        self.access_times[key] = time.time()
        
        print(f"💾 Сохранено в кэш: {key}")
    
    async def clear(self):
        """Очистка кэша"""
        self.cache.clear()
        self.access_times.clear()
        print("🧹 Кэш очищен")
    
    def get_stats(self) -> Dict:
        """Получение статистики кэша"""
        return {
            'total_entries': len(self.cache),
            'max_size': self.max_size,
            'hit_rate': self._calculate_hit_rate(),
            'avg_access_time': self._calculate_avg_access_time()
        }
    
    def _calculate_hit_rate(self) -> float:
        """Расчет хит-рейта"""
        if not self.access_times:
            return 0.0
        
        total_accesses = sum(self.access_times.values())
        if total_accesses == 0:
            return 0.0
        
        hit_count = len([t for t in self.access_times.values() if t > 0])
        return hit_count / len(self.access_times)
    
    def _calculate_avg_access_time(self) -> float:
        """Расчет среднего времени доступа"""
        if not self.access_times:
            return 0.0
        
        return sum(self.access_times.values()) / len(self.access_times)

# Интеграция с сетью
class CachedNetwork:
    """Сеть с поддержкой кэширования"""
    
    def __init__(self, network, cache: TaskCache):
        self.network = network
        self.cache = cache
    
    async def submit_task(self, task_data: Dict) -> str:
        """Подача задачи с проверкой кэша"""
        # Проверяем наличие в кэше
        cached_result = await self.cache.get(task_data)
        
        if cached_result is not None:
            print(f"✅ Результат из кэша")
            # Возвращаем ID задачи с кэшированным результатом
            return f"cached_{hash(str(task_data))}"
        
        # Подаем задачу в сеть
        task_id = await self.network.submit_task(task_data)
        
        # Сохраняем результат в кэше после выполнения
        # Здесь нужно будет добавить обработку результата
        return task_id
```

### Оптимизация памяти

#### 1. Управление памятью

```python
import asyncio
import psutil
import gc
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class MemoryManager:
    """Менеджер памяти"""
    
    def __init__(self, max_memory_percent: float = 80.0):
        self.max_memory_percent = max_memory_percent
        self.memory_history: List[float] = []
        self.running = False
    
    async def start(self):
        """Запуск мониторинга памяти"""
        self.running = True
        
        asyncio.create_task(self.monitor_memory())
        asyncio.create_task(self.optimize_memory())
        
        print("🧠 Менеджер памяти запущен")
    
    async def stop(self):
        """Остановка менеджера памяти"""
        self.running = False
    
    async def monitor_memory(self):
        """Мониторинг использования памяти"""
        while self.running:
            try:
                # Получаем информацию о памяти
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                
                # Сохраняем историю
                self.memory_history.append(memory_percent)
                
                # Ограничиваем историю
                if len(self.memory_history) > 100:
                    self.memory_history.pop(0)
                
                # Выводим информацию
                print(f"📊 Использование памяти: {memory_percent:.1f}%")
                
                await asyncio.sleep(30)  # Мониторинг каждые 30 секунд
                
            except Exception as e:
                print(f"❌ Ошибка мониторинга памяти: {e}")
                await asyncio.sleep(60)
    
    async def optimize_memory(self):
        """Оптимизация использования памяти"""
        while self.running:
            try:
                # Проверяем использование памяти
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                
                if memory_percent > self.max_memory_percent:
                    print(f"⚠️ Высокое использование памяти: {memory_percent:.1f}%")
                    
                    # Запускаем оптимизацию
                    await self.perform_memory_optimization()
                
                await asyncio.sleep(60)  # Проверка каждые 60 секунд
                
            except Exception as e:
                print(f"❌ Ошибка оптимизации памяти: {e}")
                await asyncio.sleep(120)
    
    async def perform_memory_optimization(self):
        """Выполнение оптимизации памяти"""
        print("🔧 Выполнение оптимизации памяти...")
        
        try:
            # 1. Сбор мусора
            collected = gc.collect()
            print(f"🗑️ Собрано мусора: {collected} объектов")
            
            # 2. Очистка кэша (если есть)
            if hasattr(self, 'cache'):
                await self.cache.clear()
            
            # 3. Оптимизация данных в памяти
            await self.optimize_data_structures()
            
            # 4. Сжатие данных
            await self.compress_data()
            
            print("✅ Оптимизация памяти завершена")
            
        except Exception as e:
            print(f"❌ Ошибка оптимизации памяти: {e}")
    
    async def optimize_data_structures(self):
        """Оптимизация структур данных"""
        # Здесь можно реализовать оптимизацию конкретных структур данных
        # Например, сжатие списков, удаление дубликатов и т.д.
        
        print("🔧 Оптимизация структур данных...")
        
        # Пример: очистка списков
        if hasattr(self, 'large_lists'):
            for name, lst in self.large_lists.items():
                if len(lst) > 10000:
                    # Очистка старых элементов
                    lst = [item for item in lst if time.time() - item.get('timestamp', 0) < 3600]
                    self.large_lists[name] = lst
                    print(f"🧹 Очищен список {name}: {len(lst)} элементов")
    
    async def compress_data(self):
        """Сжатие данных в памяти"""
        print("🗜️ Сжатие данных...")
        
        # Здесь можно реализовать сжатие больших структур данных
        # Например, сжатие строк, числовых данных и т.д.
        
        # Пример: сжатие строк
        if hasattr(self, 'string_data'):
            for key, data in self.string_data.items():
                if isinstance(data, str) and len(data) > 1000:
                    # Простое сжатие (в реальной системе использовать zlib/gzip)
                    compressed = data[:100] + "...[сжато]..."
                    self.string_data[key] = compressed
                    print(f"🗜️ Сжата строка {key}: {len(data)} -> {len(compressed)} символов")
```

---

## 🔌 Интеграция с внешними системами

### REST API сервер

#### 1. FastAPI сервер

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import asyncio
import json
import time
from contextlib import asynccontextmanager

# Импортируем нашу сеть
from main import ComputeNetwork
from core.task import Task, TaskType, TaskPriority

# Глобальная переменная для сети
network = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запуск при старте
    global network
    network = ComputeNetwork(host='0.0.0.0', port=5555)
    await network.start()
    print("🚀 Compute Network API запущен")
    
    yield
    
    # Остановка при завершении
    await network.stop()
    print("🛑 Compute Network API остановлен")

# Создаем FastAPI приложение
app = FastAPI(
    title="Compute Network API",
    description="API для децентрализованной вычислительной сети",
    version="1.0.0",
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic модели
class TaskRequest(BaseModel):
    task_type: str
    owner_id: str
    parameters: Dict[str, Any]
    requirements: Dict[str, float]
    config: Dict[str, Any]

class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str

class NetworkStatus(BaseModel):
    node_id: str
    host: str
    port: int
    peers_count: int
    active_tasks: int
    credits: float
    reputation_score: float

class BatchRequest(BaseModel):
    tasks: List[TaskRequest]

# API эндпоинты

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "Compute Network API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Проверка здоровья API"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "network_running": network is not None
    }

@app.post("/api/v1/tasks", response_model=TaskResponse)
async def submit_task(task_request: TaskRequest):
    """Подача задачи"""
    try:
        # Преобразование запроса в задачу
        task = Task.create_task_from_request(task_request)
        
        # Подача в сеть
        task_id = await network.submit_task(task.to_dict())
        
        return TaskResponse(
            task_id=task_id,
            status="pending",
            message="Task submitted successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Получение статуса задачи"""
    try:
        status = await network.get_task_status(task_id)
        return status
        
    except Exception as e:
        raise HTTPException(status_code=404, detail="Task not found")

@app.get("/api/v1/network/status")
async def get_network_status():
    """Получение статуса сети"""
    try:
        status = await network.get_network_status()
        return status
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/tasks/batch", response_model=List[TaskResponse])
async def submit_batch_tasks(batch_request: BatchRequest):
    """Пакетная подача задач"""
    responses = []
    
    for task_request in batch_request.tasks:
        try:
            task = Task.create_task_from_request(task_request)
            task_id = await network.submit_task(task.to_dict())
            
            responses.append(TaskResponse(
                task_id=task_id,
                status="pending",
                message="Task submitted successfully"
            ))
            
        except Exception as e:
            responses.append(TaskResponse(
                task_id="",
                status="error",
                message=str(e)
            ))
    
    return responses

@app.get("/api/v1/network/metrics")
async def get_network_metrics():
    """Получение метрик сети"""
    try:
        # Получаем различные метрики
        status = await network.get_network_status()
        pricing_analytics = network.pricing_engine.get_pricing_analytics()
        credit_health = network.credit_manager.get_network_health()
        
        return {
            "network_status": status,
            "pricing_analytics": pricing_analytics,
            "credit_health": credit_health,
            "timestamp": time.time()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/reputation/{node_id}")
async def get_node_reputation(node_id: str):
    """Получение репутации узла"""
    try:
        score = await network.reputation_manager.get_reputation_score(node_id)
        level = await network.reputation_manager.get_reputation_level(node_id)
        
        return {
            "node_id": node_id,
            "reputation_score": score,
            "reputation_level": level,
            "timestamp": time.time()
        }
        
    except Exception as e:
        raise HTTPException(status_code=404, detail="Node not found")

@app.post("/api/v1/tasks/{task_id}/cancel")
async def cancel_task(task_id: str, reason: str):
    """Отмена задачи"""
    try:
        await network.cancel_task(task_id, reason)
        return {"message": f"Task {task_id} cancelled successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/types")
async def get_task_types():
    """Получение поддерживаемых типов задач"""
    return {
        "task_types": [t.value for t in TaskType],
        "priorities": [p.value for p in TaskPriority]
    }

@app.get("/api/v1/examples")
async def get_task_examples():
    """Получение примеров задач"""
    return {
        "examples": {
            "range_reduce": {
                "description": "Операции над диапазоном чисел",
                "parameters": {
                    "start": "Начальное значение",
                    "end": "Конечное значение",
                    "operation": "Операция (sum, product, min, max, average)"
                }
            },
            "map": {
                "description": "Применение функции к каждому элементу",
                "parameters": {
                    "data": "Набор данных",
                    "function": "Функция для применения"
                }
            },
            "ml_inference": {
                "description": "Инференс нейронных сетей",
                "parameters": {
                    "model_path": "Путь к модели",
                    "input_data": "Входные данные",
                    "model_type": "Тип модели (pytorch, tensorflow)"
                }
            }
        }
    }

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### 2. GraphQL API

```python
from fastapi import FastAPI
from fastapi.graphql import GraphQLApp
from graphql import (
    GraphQLSchema,
    GraphQLObjectType,
    GraphQLField,
    GraphQLString,
    GraphQLList,
    GraphQLNonNull,
    GraphQLArgument,
    GraphQLResolveInfo,
    graphql_sync
)
import json

# GraphQL схема
TaskType = GraphQLObjectType(
    name="Task",
    fields={
        "task_id": GraphQLField(GraphQLNonNull(GraphQLString)),
        "status": GraphQLField(GraphQLString),
        "owner_id": GraphQLField(GraphQLString),
        "task_type": GraphQLField(GraphQLString),
        "result": GraphQLField(GraphQLString),
        "created_at": GraphQLField(GraphQLString),
        "updated_at": GraphQLField(GraphQLString),
    }
)

NetworkStatusType = GraphQLObjectType(
    name="NetworkStatus",
    fields={
        "node_id": GraphQLField(GraphQLNonNull(GraphQLString)),
        "peers_count": GraphQLField(GraphQLNonNull(GraphQLString)),
        "active_tasks": GraphQLField(GraphQLNonNull(GraphQLString)),
        "credits": GraphQLField(GraphQLNonNull(GraphQLString)),
        "reputation_score": GraphQLField(GraphQLNonNull(GraphQLString)),
    }
)

# Резолверы
def resolve_tasks(root, info: GraphQLResolveInfo, **args):
    """Получение списка задач"""
    try:
        # Здесь должна быть логика получения задач
        return []
    except Exception as e:
        raise Exception(f"Error fetching tasks: {e}")

def resolve_task(root, info: GraphQLResolveInfo, **args):
    """Получение конкретной задачи"""
    task_id = args.get("task_id")
    try:
        # Здесь должна быть логика получения задачи
        return None
    except Exception as e:
        raise Exception(f"Error fetching task {task_id}: {e}")

def resolve_network_status(root, info: GraphQLResolveInfo, **args):
    """Получение статуса сети"""
    try:
        # Здесь должна быть логика получения статуса сети
        return {}
    except Exception as e:
        raise Exception(f"Error fetching network status: {e}")

# Определение схем
schema = GraphQLSchema(
    query=GraphQLObjectType(
        name="Query",
        fields={
            "tasks": GraphQLField(
                GraphQLList(TaskType),
                resolve=resolve_tasks
            ),
            "task": GraphQLField(
                TaskType,
                args={"task_id": GraphQLArgument(GraphQLNonNull(GraphQLString))},
                resolve=resolve_task
            ),
            "networkStatus": GraphQLField(
                NetworkStatusType,
                resolve=resolve_network_status
            )
        }
    ),
    mutation=GraphQLObjectType(
        name="Mutation",
        fields={
            "submitTask": GraphQLField(
                TaskType,
                args={
                    "task_type": GraphQLArgument(GraphQLNonNull(GraphQLString)),
                    "owner_id": GraphQLArgument(GraphQLNonNull(GraphQLString)),
                    "parameters": GraphQLArgument(GraphQLNonNull(GraphQLString)),
                },
                resolve=lambda root, info, **args: submit_task_mutation(root, info, **args)
            )
        }
    )
)

# Мутация
def submit_task_mutation(root, info: GraphQLResolveInfo, **args):
    """Подача задачи через GraphQL"""
    try:
        task_data = {
            "task_type": args["task_type"],
            "owner_id": args["owner_id"],
            "parameters": json.loads(args["parameters"])
        }
        
        # Здесь должна быть логика подачи задачи
        return {"task_id": "generated_id", "status": "pending"}
        
    except Exception as e:
        raise Exception(f"Error submitting task: {e}")

# Создание FastAPI приложения
app = FastAPI()

# Добавление GraphQL эндпоинта
app.add_route("/graphql", GraphQLApp(schema=schema))
```

### Интеграция с базами данных

#### 1. PostgreSQL интеграция

```python
import asyncpg
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json
import time

@dataclass
class TaskRecord:
    """Запись задачи в БД"""
    id: int
    task_id: str
    owner_id: str
    task_type: str
    status: str
    result: Optional[Dict[str, Any]]
    created_at: float
    updated_at: float
    execution_time: Optional[float] = None

class DatabaseManager:
    """Менеджер базы данных"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None
    
    async def initialize(self):
        """Инициализация подключения к БД"""
        self.pool = await asyncpg.create_pool(self.database_url)
        
        # Создание таблиц
        async with self.pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    task_id VARCHAR(255) UNIQUE,
                    owner_id VARCHAR(255),
                    task_type VARCHAR(50),
                    status VARCHAR(50),
                    result JSONB,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW(),
                    execution_time FLOAT,
                    credits_used FLOAT DEFAULT 0.0
                )
            ''')
            
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS nodes (
                    id SERIAL PRIMARY KEY,
                    node_id VARCHAR(255) UNIQUE,
                    host VARCHAR(50),
                    port INTEGER,
                    capabilities JSONB,
                    reputation_score FLOAT DEFAULT 0.5,
                    last_seen TIMESTAMP DEFAULT NOW(),
                    credits_balance FLOAT DEFAULT 0.0
                )
            ''')
            
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS credit_transfers (
                    id SERIAL PRIMARY KEY,
                    from_node_id VARCHAR(255),
                    to_node_id VARCHAR(255),
                    amount FLOAT,
                    task_id VARCHAR(255),
                    timestamp TIMESTAMP DEFAULT NOW()
                )
            ''')
    
    async def save_task(self, task: TaskRecord):
        """Сохранение задачи в БД"""
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO tasks (task_id, owner_id, task_type, status, result, execution_time)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (task_id) DO UPDATE SET
                    status = $4,
                    result = $5,
                    execution_time = $6,
                    updated_at = NOW()
            ''', task.task_id, task.owner_id, task.task_type, task.status, 
            json.dumps(task.result) if task.result else None, task.execution_time)
    
    async def get_task(self, task_id: str) -> Optional[TaskRecord]:
        """Получение задачи из БД"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow('''
                SELECT * FROM tasks WHERE task_id = $1
            ''', task_id)
            
            if row:
                return TaskRecord(
                    id=row['id'],
                    task_id=row['task_id'],
                    owner_id=row['owner_id'],
                    task_type=row['task_type'],
                    status=row['status'],
                    result=row['result'],
                    created_at=row['created_at'].timestamp(),
                    updated_at=row['updated_at'].timestamp(),
                    execution_time=row['execution_time']
                )
            
            return None
    
    async def get_tasks_by_owner(self, owner_id: str, limit: int = 100) -> List[TaskRecord]:
        """Получение задач владельца"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch('''
                SELECT * FROM tasks WHERE owner_id = $1
                ORDER BY created_at DESC
                LIMIT $2
            ''', owner_id, limit)
            
            tasks = []
            for row in rows:
                task = TaskRecord(
                    id=row['id'],
                    task_id=row['task_id'],
                    owner_id=row['owner_id'],
                    task_type=row['task_type'],
                    status=row['status'],
                    result=row['result'],
                    created_at=row['created_at'].timestamp(),
                    updated_at=row['updated_at'].timestamp(),
                    execution_time=row['execution_time']
                )
                tasks.append(task)
            
            return tasks
    
    async def save_node(self, node_id: str, host: str, port: int, capabilities: Dict):
        """Сохранение узла в БД"""
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO nodes (node_id, host, port, capabilities)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (node_id) DO UPDATE SET
                    host = $2,
                    port = $3,
                    capabilities = $4,
                    last_seen = NOW()
            ''', node_id, host, port, json.dumps(capabilities))
    
    async def get_node(self, node_id: str) -> Optional[Dict]:
        """Получение узла из БД"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow('''
                SELECT * FROM nodes WHERE node_id = $1
            ''', node_id)
            
            return dict(row) if row else None
    
    async def record_credit_transfer(self, from_node_id: str, to_node_id: str, amount: float, task_id: str):
        """Запись перевода кредитов"""
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO credit_transfers (from_node_id, to_node_id, amount, task_id)
                VALUES ($1, $2, $3, $4)
            ''', from_node_id, to_node_id, amount, task_id)
    
    async def get_credit_history(self, node_id: str, limit: int = 100) -> List[Dict]:
        """Получение истории кредитов узла"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch('''
                SELECT * FROM credit_transfers
                WHERE from_node_id = $1 OR to_node_id = $1
                ORDER BY timestamp DESC
                LIMIT $2
            ''', node_id, limit)
            
            return [dict(row) for row in rows]
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Получение статистики системы"""
        async with self.pool.acquire() as conn:
            # Статистика задач
            task_stats = await conn.fetch('''
                SELECT 
                    COUNT(*) as total_tasks,
                    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_tasks,
                    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_tasks,
                    AVG(execution_time) as avg_execution_time
                FROM tasks
            ''')
            
            # Статистика узлов
            node_stats = await conn.fetch('''
                SELECT 
                    COUNT(*) as total_nodes,
                    AVG(reputation_score) as avg_reputation,
                    SUM(credits_balance) as total_credits
                FROM nodes
            ''')
            
            # Статистика кредитов
            credit_stats = await conn.fetch('''
                SELECT 
                    COUNT(*) as total_transfers,
                    SUM(amount) as total_amount,
                    AVG(amount) as avg_amount
                FROM credit_transfers
            ''')
            
            return {
                "tasks": dict(task_stats[0]),
                "nodes": dict(node_stats[0]),
                "credits": dict(credit_stats[0])
            }
    
    async def close(self):
        """Закрытие подключения"""
        if self.pool:
            await self.pool.close()
```

#### 2. Redis для кэширования

```python
import redis.asyncio as redis
import json
import time
from typing import Optional, Dict, Any

class RedisCache:
    """Кэш на основе Redis"""
    
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.default_ttl = 3600  # 1 час
    
    async def initialize(self):
        """Инициализация подключения"""
        await self.redis.ping()
        print("✅ Redis подключен")
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Установка значения в кэш"""
        if ttl is None:
            ttl = self.default_ttl
        
        value_json = json.dumps(value, default=str)
        await self.redis.setex(key, ttl, value_json)
    
    async def get(self, key: str) -> Optional[Any]:
        """Получение значения из кэша"""
        value_json = await self.redis.get(key)
        
        if value_json is None:
            return None
        
        return json.loads(value_json)
    
    async def delete(self, key: str):
        """Удаление значения из кэша"""
        await self.redis.delete(key)
    
    async def exists(self, key: str) -> bool:
        """Проверка существования ключа"""
        return await self.redis.exists(key) > 0
    
    async def expire(self, key: str, ttl: int):
        """Установка времени жизни ключа"""
        await self.redis.expire(key, ttl)
    
    async def ttl(self, key: str) -> int:
        """Получение времени жизни ключа"""
        return await self.redis.ttl(key)
    
    async def incr(self, key: str, amount: int = 1) -> int:
        """Инкремент значения"""
        return await self.redis.incr(key, amount)
    
    async def decr(self, key: str, amount: int = 1) -> int:
        """Декремент значения"""
        return await self.redis.decr(key, amount)
    
    async def hset(self, key: str, field: str, value: Any):
        """Установка поля в хэше"""
        value_json = json.dumps(value, default=str)
        await self.redis.hset(key, field, value_json)
    
    async def hget(self, key: str, field: str) -> Optional[Any]:
        """Получение поля из хэша"""
        value_json = await self.redis.hget(key, field)
        
        if value_json is None:
            return None
        
        return json.loads(value_json)
    
    async def hgetall(self, key: str) -> Dict[str, Any]:
        """Получение всех полей хэша"""
        fields = await self.redis.hgetall(key)
        
        result = {}
        for field, value_json in fields.items():
            result[field] = json.loads(value_json)
        
        return result
    
    async def lpush(self, key: str, values: list):
        """Добавление элементов в начало списка"""
        values_json = [json.dumps(value, default=str) for value in values]
        await self.redis.lpush(key, *values_json)
    
    async def rpop(self, key: str) -> Optional[Any]:
        """Получение элемента из конца списка"""
        value_json = await self.redis.rpop(key)
        
        if value_json is None:
            return None
        
        return json.loads(value_json)
    
    async def llen(self, key: str) -> int:
        """Получение длины списка"""
        return await self.redis.llen(key)
    
    async def flushdb(self):
        """Очистка базы данных"""
        await self.redis.flushdb()
    
    async def close(self):
        """Закрытие подключения"""
        await self.redis.close()
```

### Webhook уведомления

```python
import aiohttp
import asyncio
from typing import Dict, Any, Optional
from dataclasses import dataclass
import json
import time

@dataclass
class WebhookConfig:
    """Конфигурация вебхука"""
    url: str
    method: str = "POST"
    headers: Dict[str, str] = None
    timeout: int = 30
    retry_count: int = 3
    retry_delay: int = 5

class WebhookManager:
    """Менеджер вебхуков"""
    
    def __init__(self, config: WebhookConfig):
        self.config = config
        self.session = None
    
    async def initialize(self):
        """Инициализация сессии"""
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)
        self.session = aiohttp.ClientSession(timeout=timeout)
    
    async def send_notification(self, event_type: str, data: Dict[str, Any]) -> bool:
        """Отправка уведомления"""
        try:
            # Подготовка payload
            payload = {
                "event_type": event_type,
                "timestamp": time.time(),
                "data": data
            }
            
            # Отправка запроса
            async with self.session.request(
                method=self.config.method,
                url=self.config.url,
                json=payload,
                headers=self.config.headers or {}
            ) as response:
                if response.status == 200:
                    print(f"✅ Уведомление отправлено: {event_type}")
                    return True
                else:
                    print(f"❌ Ошибка отправки уведомления: {response.status}")
                    return False
        
        except Exception as e:
            print(f"❌ Ошибка отправки вебхука: {e}")
            return False
    
    async def send_task_notification(self, task_id: str, status: str, result: Optional[Dict] = None):
        """Отправка уведомления о задаче"""
        data = {
            "task_id": task_id,
            "status": status,
            "result": result
        }
        
        await self.send_notification("task_update", data)
    
    async def send_network_notification(self, event_type: str, data: Dict):
        """Отправка уведомления о сети"""
        await self.send_notification(f"network_{event_type}", data)
    
    async def send_credit_notification(self, from_node: str, to_node: str, amount: float, task_id: str):
        """Отправка уведомления о переводе кредитов"""
        data = {
            "from_node": from_node,
            "to_node": to_node,
            "amount": amount,
            "task_id": task_id
        }
        
        await self.send_notification("credit_transfer", data)
    
    async def close(self):
        """Закрытие сессии"""
        if self.session:
            await self.session.close()

# Пример использования
async def webhook_example():
    # Конфигурация вебхука
    config = WebhookConfig(
        url="https://example.com/webhooks",
        method="POST",
        headers={"Authorization": "Bearer secret_token"},
        timeout=10,
        retry_count=3
    )
    
    # Создаем менеджер
    webhook_manager = WebhookManager(config)
    await webhook_manager.initialize()
    
    try:
        # Отправка уведомления о задаче
        await webhook_manager.send_task_notification(
            task_id="task_123",
            status="completed",
            result={"result": "success", "execution_time": 2.5}
        )
        
        # Отправка уведомления о сети
        await webhook_manager.send_network_notification(
            event_type="node_joined",
            data={"node_id": "node_456", "timestamp": time.time()}
        )
        
        # Отправка уведомления о кредитах
        await webhook_manager.send_credit_notification(
            from_node="node_123",
            to_node="node_456",
            amount=10.5,
            task_id="task_789"
        )
        
    finally:
        await webhook_manager.close()
```

---

## 🎨 Кастомизация и расширение

### Плагины для расширения функциональности

#### 1. Система плагинов

```python
import asyncio
import importlib
import inspect
from typing import Dict, List, Any, Optional, Type
from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging

@dataclass
class PluginConfig:
    """Конфигурация плагина"""
    name: str
    version: str
    enabled: bool = True
    config: Dict[str, Any] = None

class PluginInterface(ABC):
    """Интерфейс плагина"""
    
    @abstractmethod
    async def initialize(self, config: Dict[str, Any]) -> None:
        """Инициализация плагина"""
        pass
    
    @abstractmethod
    async def execute(self, data: Any) -> Any:
        """Выполнение плагина"""
        pass
    
    @abstractmethod
    async def cleanup(self) -> None:
        """Очистка ресурсов"""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Имя плагина"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Версия плагина"""
        pass

class PluginManager:
    """Менеджер плагинов"""
    
    def __init__(self):
        self.plugins: Dict[str, PluginInterface] = {}
        self.plugin_configs: Dict[str, PluginConfig] = {}
        self.logger = logging.getLogger(__name__)
    
    async def load_plugin(self, plugin_class: Type[PluginInterface], config: PluginConfig) -> bool:
        """Загрузка плагина"""
        try:
            # Создание экземпляра плагина
            plugin_instance = plugin_class()
            
            # Инициализация
            await plugin_instance.initialize(config.config or {})
            
            # Сохранение
            self.plugins[config.name] = plugin_instance
            self.plugin_configs[config.name] = config
            
            self.logger.info(f"✅ Плагин {config.name} v{config.version} загружен")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка загрузки плагина {config.name}: {e}")
            return False
    
    async def unload_plugin(self, plugin_name: str) -> bool:
        """Выгрузка плагина"""
        try:
            if plugin_name in self.plugins:
                # Очистка плагина
                await self.plugins[plugin_name].cleanup()
                
                # Удаление
                del self.plugins[plugin_name]
                del self.plugin_configs[plugin_name]
                
                self.logger.info(f"✅ Плагин {plugin_name} выгружен")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка выгрузки плагина {plugin_name}: {e}")
            return False
    
    async def execute_plugin(self, plugin_name: str, data: Any) -> Any:
        """Выполнение плагина"""
        try:
            if plugin_name not in self.plugins:
                raise ValueError(f"Плагин {plugin_name} не найден")
            
            if not self.plugin_configs[plugin_name].enabled:
                raise ValueError(f"Плагин {plugin_name} отключен")
            
            # Выполнение
            result = await self.plugins[plugin_name].execute(data)
            
            self.logger.debug(f"🔌 Плагин {plugin_name} выполнен успешно")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка выполнения плагина {plugin_name}: {e}")
            raise
    
    def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """Получение информации о плагине"""
        if plugin_name in self.plugins:
            return {
                "name": self.plugins[plugin_name].name,
                "version": self.plugins[plugin_name].version,
                "enabled": self.plugin_configs[plugin_name].enabled,
                "config": self.plugin_configs[plugin_name].config
            }
        return None
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        """Список всех плагинов"""
        plugins_info = []
        for name in self.plugins:
            info = self.get_plugin_info(name)
            if info:
                plugins_info.append(info)
        return plugins_info
    
    async def reload_plugin(self, plugin_name: str) -> bool:
        """Перезагрузка плагина"""
        try:
            if plugin_name in self.plugins:
                # Сохраняем конфигурацию
                config = self.plugin_configs[plugin_name]
                
                # Выгружаем
                await self.unload_plugin(plugin_name)
                
                # Загружаем заново
                return await self.load_plugin(self.plugins[plugin_name].__class__, config)
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка перезагрузки плагина {plugin_name}: {e}")
            return False
```

#### 2. Пример плагина для обработки данных

```python
import numpy as np
from typing import Dict, Any
from plugin_manager import PluginInterface, PluginConfig

class DataProcessorPlugin(PluginInterface):
    """Плагин для обработки данных"""
    
    def __init__(self):
        self.config = None
    
    async def initialize(self, config: Dict[str, Any]) -> None:
        """Инициализация плагина"""
        self.config = config
        
        # Параметры обработки
        self.normalization_method = config.get('normalization_method', 'minmax')
        self.outlier_detection = config.get('outlier_detection', True)
        self.outlier_threshold = config.get('outlier_threshold', 3.0)
        
        print(f"🔧 Плагин DataProcessor инициализирован")
    
    async def execute(self, data: Any) -> Any:
        """Выполнение обработки данных"""
        try:
            # Преобразование в numpy array
            if isinstance(data, list):
                data_array = np.array(data)
            elif isinstance(data, np.ndarray):
                data_array = data
            else:
                raise ValueError("Unsupported data type")
            
            # Нормализация
            if self.normalization_method == 'minmax':
                data_array = self._minmax_normalize(data_array)
            elif self.normalization_method == 'zscore':
                data_array = self._zscore_normalize(data_array)
            
            # Обнаружение выбросов
            if self.outlier_detection:
                data_array = self._remove_outliers(data_array)
            
            return data_array.tolist()
            
        except Exception as e:
            print(f"❌ Ошибка обработки данных: {e}")
            raise
    
    async def cleanup(self) -> None:
        """Очистка ресурсов"""
        self.config = None
        print("🧹 Плагин DataProcessor очищен")
    
    @property
    def name(self) -> str:
        return "DataProcessor"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    def _minmax_normalize(self, data: np.ndarray) -> np.ndarray:
        """Нормализация Min-Max"""
        min_val = np.min(data)
        max_val = np.max(data)
        
        if max_val == min_val:
            return np.zeros_like(data)
        
        return (data - min_val) / (max_val - min_val)
    
    def _zscore_normalize(self, data: np.ndarray) -> np.ndarray:
        """Нормализация Z-score"""
        mean = np.mean(data)
        std = np.std(data)
        
        if std == 0:
            return np.zeros_like(data)
        
        return (data - mean) / std
    
    def _remove_outliers(self, data: np.ndarray) -> np.ndarray:
        """Удаление выбросов"""
        mean = np.mean(data)
        std = np.std(data)
        
        # Границы для выбросов
        lower_bound = mean - self.outlier_threshold * std
        upper_bound = mean + self.outlier_threshold * std
        
        # Фильтрация
        mask = (data >= lower_bound) & (data <= upper_bound)
        return data[mask]
```

#### 3. Пример плагина для аутентификации

```python
from typing import Dict, Any, Optional
from plugin_manager import PluginInterface, PluginConfig
import hashlib
import time

class AuthPlugin(PluginInterface):
    """Плагин для аутентификации"""
    
    def __init__(self):
        self.users = {}
        self.sessions = {}
    
    async def initialize(self, config: Dict[str, Any]) -> None:
        """Инициализация плагина"""
        self.config = config
        
        # Загрузка пользователей из конфигурации
        for user_data in config.get('users', []):
            self._create_user(user_data['username'], user_data['password'])
        
        print(f"🔐 Плагин Auth инициализирован")
    
    async def execute(self, data: Any) -> Any:
        """Выполнение аутентификации"""
        try:
            if isinstance(data, dict):
                action = data.get('action')
                
                if action == 'login':
                    return await self._login(data['username'], data['password'])
                elif action == 'logout':
                    return await self._logout(data['session_id'])
                elif action == 'validate':
                    return await self._validate_session(data['session_id'])
                else:
                    raise ValueError("Unknown action")
            
            raise ValueError("Invalid data format")
            
        except Exception as e:
            print(f"❌ Ошибка аутентификации: {e}")
            raise
    
    async def cleanup(self) -> None:
        """Очистка ресурсов"""
        self.users.clear()
        self.sessions.clear()
        print("🧹 Плагин Auth очищен")
    
    @property
    def name(self) -> str:
        return "Auth"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    def _create_user(self, username: str, password: str):
        """Создание пользователя"""
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.users[username] = {
            'password': hashed_password,
            'created_at': time.time()
        }
    
    async def _login(self, username: str, password: str) -> Dict[str, Any]:
        """Логин пользователя"""
        if username not in self.users:
            raise ValueError("User not found")
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        if self.users[username]['password'] != hashed_password:
            raise ValueError("Invalid password")
        
        # Создание сессии
        session_id = hashlib.sha256(f"{username}{time.time()}".encode()).hexdigest()[:32]
        self.sessions[session_id] = {
            'username': username,
            'created_at': time.time(),
            'last_activity': time.time()
        }
        
        return {
            'session_id': session_id,
            'username': username,
            'expires_at': time.time() + 3600  # 1 час
        }
    
    async def _logout(self, session_id: str) -> bool:
        """Выход пользователя"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    async def _validate_session(self, session_id: str) -> Dict[str, Any]:
        """Валидация сессии"""
        if session_id not in self.sessions:
            raise ValueError("Invalid session")
        
        session = self.sessions[session_id]
        
        # Проверка времени жизни
        if time.time() - session['last_activity'] > 3600:  # 1 час
            del self.sessions[session_id]
            raise ValueError("Session expired")
        
        # Обновление активности
        session['last_activity'] = time.time()
        
        return {
            'valid': True,
            'username': session['username'],
            'expires_at': session['created_at'] + 3600
        }
```

### Кастомные типы задач

#### 1. Расширение системы задач

```python
from core.task import Task, TaskType
from typing import Dict, Any, List
import time

class CustomTaskType:
    """Класс для регистрации кастомных типов задач"""
    
    _custom_types = {}
    
    @classmethod
    def register_type(cls, task_type: str, handler_class: type):
        """Регистрация нового типа задачи"""
        cls._custom_types[task_type] = handler_class
        print(f"📝 Зарегистрирован тип задачи: {task_type}")
    
    @classmethod
    def get_handler(cls, task_type: str):
        """Получение обработчика типа задачи"""
        return cls._custom_types.get(task_type)

class DataAnalysisTask(Task):
    """Задача для анализа данных"""
    
    def __init__(self, owner_id: str, data: List, analysis_type: str, **kwargs):
        super().__init__(owner_id, TaskType.CUSTOM, **kwargs)
        self.data = data
        self.analysis_type = analysis_type
    
    def validate(self) -> List[str]:
        """Валидация задачи"""
        errors = []
        
        if not isinstance(self.data, list):
            errors.append("Data must be a list")
        
        if not self.analysis_type:
            errors.append("Analysis type is required")
        
        # Дополнительная валидация в зависимости от типа анализа
        if self.analysis_type == "statistical":
            if len(self.data) < 2:
                errors.append("Statistical analysis requires at least 2 data points")
        
        return errors
    
    def execute(self) -> Dict[str, Any]:
        """Выполнение анализа"""
        if self.analysis_type == "statistical":
            return self._statistical_analysis()
        elif self.analysis_type == "correlation":
            return self._correlation_analysis()
        else:
            raise ValueError(f"Unknown analysis type: {self.analysis_type}")
    
    def _statistical_analysis(self) -> Dict[str, Any]:
        """Статистический анализ"""
        import numpy as np
        
        data_array = np.array(self.data)
        
        return {
            'mean': float(np.mean(data_array)),
            'median': float(np.median(data_array)),
            'std': float(np.std(data_array)),
            'min': float(np.min(data_array)),
            'max': float(np.max(data_array)),
            'count': len(data_array),
            'timestamp': time.time()
        }
    
    def _correlation_analysis(self) -> Dict[str, Any]:
        """Анализ корреляции"""
        import numpy as np
        from scipy import stats
        
        if len(self.data) < 2:
            raise ValueError("Correlation analysis requires at least 2 datasets")
        
        # Предполагаем, что данные в формате [x1, x2, x3, ...]
        x = self.data[0]
        y = self.data[1]
        
        correlation, p_value = stats.pearsonr(x, y)
        
        return {
            'correlation': float(correlation),
            'p_value': float(p_value),
            'significant': p_value < 0.05,
            'timestamp': time.time()
        }

class ImageProcessingTask(Task):
    """Задача для обработки изображений"""
    
    def __init__(self, owner_id: str, image_path: str, operation: str, **kwargs):
        super().__init__(owner_id, TaskType.CUSTOM, **kwargs)
        self.image_path = image_path
        self.operation = operation
    
    def validate(self) -> List[str]:
        """Валидация задачи"""
        errors = []
        
        if not self.image_path:
            errors.append("Image path is required")
        
        if not self.operation:
            errors.append("Operation is required")
        
        # Проверка поддерживаемых операций
        supported_operations = ["resize", "crop", "filter", "enhance"]
        if self.operation not in supported_operations:
            errors.append(f"Unsupported operation: {self.operation}")
        
        return errors
    
    def execute(self) -> Dict[str, Any]:
        """Выполнение обработки изображения"""
        try:
            from PIL import Image
            
            with Image.open(self.image_path) as img:
                if self.operation == "resize":
                    return self._resize_image(img)
                elif self.operation == "crop":
                    return self._crop_image(img)
                elif self.operation == "filter":
                    return self._apply_filter(img)
                elif self.operation == "enhance":
                    return self._enhance_image(img)
                else:
                    raise ValueError(f"Unknown operation: {self.operation}")
        
        except Exception as e:
            raise RuntimeError(f"Image processing failed: {e}")
    
    def _resize_image(self, img) -> Dict[str, Any]:
        """Изменение размера изображения"""
        # Пример: изменение размера до 800x600
        resized = img.resize((800, 600))
        
        return {
            'operation': 'resize',
            'original_size': img.size,
            'new_size': resized.size,
            'timestamp': time.time()
        }
    
    def _crop_image(self, img) -> Dict[str, Any]:
        """Обрезка изображения"""
        # Пример: обрезка центральной части
        width, height = img.size
        left = width // 4
        top = height // 4
        right = 3 * width // 4
        bottom = 3 * height // 4
        
        cropped = img.crop((left, top, right, bottom))
        
        return {
            'operation': 'crop',
            'original_size': img.size,
            'new_size': cropped.size,
            'timestamp': time.time()
        }
    
    def _apply_filter(self, img) -> Dict[str, Any]:
        """Применение фильтра"""
        # Пример: применение размытия
        from PIL import ImageFilter
        filtered = img.filter(ImageFilter.BLUR)
        
        return {
            'operation': 'filter',
            'filter_type': 'blur',
            'original_size': img.size,
            'new_size': filtered.size,
            'timestamp': time.time()
        }
    
    def _enhance_image(self, img) -> Dict[str, Any]:
        """Улучшение изображения"""
        # Пример: улучшение контраста
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(img)
        enhanced = enhancer.enhance(1.5)
        
        return {
            'operation': 'enhance',
            'enhancement_type': 'contrast',
            'factor': 1.5,
            'original_size': img.size,
            'new_size': enhanced.size,
            'timestamp': time.time()
        }

# Регистрация кастомных типов задач
CustomTaskType.register_type("data_analysis", DataAnalysisTask)
CustomTaskType.register_type("image_processing", ImageProcessingTask)
```

#### 2. Фабрика задач

```python
from typing import Dict, Any, Type, Optional
from core.task import Task, TaskType
from custom_tasks import DataAnalysisTask, ImageProcessingTask

class TaskFactory:
    """Фабрика для создания задач"""
    
    _task_classes: Dict[TaskType, Type[Task]] = {}
    _custom_task_classes: Dict[str, Type[Task]] = {}
    
    @classmethod
    def register_task_class(cls, task_type: TaskType, task_class: Type[Task]):
        """Регистрация класса задачи"""
        cls._task_classes[task_type] = task_class
        print(f"📝 Зарегистрирован класс задачи: {task_type.value}")
    
    @classmethod
    def register_custom_task_class(cls, task_type: str, task_class: Type[Task]):
        """Регистрация кастомного класса задачи"""
        cls._custom_task_classes[task_type] = task_class
        print(f"📝 Зарегистрирован кастомный класс задачи: {task_type}")
    
    @classmethod
    def create_task(cls, task_type: str, owner_id: str, **kwargs) -> Task:
        """Создание задачи"""
        # Проверка кастомных типов
        if task_type in cls._custom_task_classes:
            task_class = cls._custom_task_classes[task_type]
            return task_class(owner_id, **kwargs)
        
        # Проверка стандартных типов
        try:
            enum_type = TaskType(task_type)
            if enum_type in cls._task_classes:
                task_class = cls._task_classes[enum_type]
                return task_class(owner_id, **kwargs)
        except ValueError:
            pass
        
        raise ValueError(f"Unknown task type: {task_type}")
    
    @classmethod
    def get_supported_types(cls) -> List[str]:
        """Получение поддерживаемых типов задач"""
        # Стандартные типы
        standard_types = [t.value for t in TaskType]
        
        # Кастомные типы
        custom_types = list(cls._custom_task_classes.keys())
        
        return standard_types + custom_types

# Регистрация стандартных типов задач
TaskFactory.register_task_class(TaskType.RANGE_REDUCE, Task)
TaskFactory.register_task_class(TaskType.MAP, Task)
TaskFactory.register_task_class(TaskType.MAP_REDUCE, Task)
TaskFactory.register_task_class(TaskType.MATRIX_OPS, Task)
TaskFactory.register_task_class(TaskType.ML_INFERENCE, Task)
TaskFactory.register_task_class(TaskType.ML_TRAIN_STEP, Task)

# Регистрация кастомных типов
TaskFactory.register_custom_task_class("data_analysis", DataAnalysisTask)
TaskFactory.register_custom_task_class("image_processing", ImageProcessingTask)
```

---

## 📊 Мониторинг и аналитика

### Система мониторинга

#### 1. Сбор метрик

```python
import asyncio
import time
import psutil
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from collections import deque
import threading

@dataclass
class SystemMetrics:
    """Метрики системы"""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_io: Dict[str, float]
    process_count: int
    load_average: List[float]

@dataclass
class NetworkMetrics:
    """Метрики сети"""
    timestamp: float
    active_tasks: int
    pending_tasks: int
    completed_tasks: int
    failed_tasks: int
    total_nodes: int
    average_response_time: float
    throughput: float

@dataclass
class TaskMetrics:
    """Метрики задач"""
    timestamp: float
    task_type: str
    execution_time: float
    resource_usage: Dict[str, float]
    success_rate: float
    queue_length: int

class MetricsCollector:
    """Сборщик метрик"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.system_metrics: deque = deque(maxlen=max_history)
        self.network_metrics: deque = deque(maxlen=max_history)
        self.task_metrics: deque = deque(maxlen=max_history)
        self.running = False
        self.collection_interval = 30  # 30 секунд
        
    async def start(self):
        """Запуск сбора метрик"""
        self.running = True
        asyncio.create_task(self._collect_metrics())
        print("📊 Сборщик метрик запущен")
    
    async def stop(self):
        """Остановка сбора метрик"""
        self.running = False
        print("📊 Сборщик метрик остановлен")
    
    async def _collect_metrics(self):
        """Сбор метрик"""
        while self.running:
            try:
                # Сбор системных метрик
                system_metrics = self._collect_system_metrics()
                self.system_metrics.append(system_metrics)
                
                # Сбор сетевых метрик
                network_metrics = self._collect_network_metrics()
                self.network_metrics.append(network_metrics)
                
                # Сбор метрик задач
                task_metrics = self._collect_task_metrics()
                self.task_metrics.append(task_metrics)
                
                print(f"📊 Метрики собраны: {time.strftime('%H:%M:%S')}")
                
                await asyncio.sleep(self.collection_interval)
                
            except Exception as e:
                print(f"❌ Ошибка сбора метрик: {e}")
                await asyncio.sleep(60)
    
    def _collect_system_metrics(self) -> SystemMetrics:
        """Сбор системных метрик"""
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Память
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # Диск
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        
        # Сеть
        network = psutil.net_io_counters()
        network_io = {
            'bytes_sent': network.bytes_sent,
            'bytes_recv': network.bytes_recv,
            'packets_sent': network.packets_sent,
            'packets_recv': network.packets_recv
        }
        
        # Процессы
