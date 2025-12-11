#!/usr/bin/env python3
"""
Основное приложение децентрализованной вычислительной сети
"""

import asyncio
import json
import time
import argparse
import signal
import sys
import os
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

# Импортируем наши модули
from core.node import ComputeNode
from core.task import Task, TaskExecutor, TaskType
from core.job import TaskStatus
from core.credits import CreditManager
from sandbox.execution import (
    SandboxExecutor,
    SandboxExecutorFactory,
    SandboxLimits,
    SandboxType,
)
from aiohttp import web
from reputation.system import ReputationManager
from pricing.dynamic import DynamicPricingEngine, PricingConfig, ResourceMetrics

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('compute_network.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ComputeNetwork:
    """Основной класс вычислительной сети"""
    
    def __init__(self, host: str = '0.0.0.0', port: int = 5555, config_file: str = None):
        self.host = host
        self.port = port
        self.running = False
        
        # Загружаем конфигурацию
        self.config = self.load_config(config_file)
        
        # Инициализируем компоненты
        self.node = ComputeNode(host, port)
        self.credit_manager = CreditManager()
        self.reputation_manager = ReputationManager()
        # Координатору нужна ссылка на ReputationManager для записи penalties
        setattr(self.node, "reputation_manager", self.reputation_manager)
        self.pricing_engine = DynamicPricingEngine(self.create_pricing_config())
        self.task_executor = TaskExecutor()
        # Подключаем песочницу к executor для внешних code_ref
        self.task_executor.sandbox_executor = None
        self.sandbox_executor = SandboxExecutorFactory.create(
            self.get_sandbox_type(),
            self.get_sandbox_limits(),
        )
        self.task_executor.sandbox_executor = self.sandbox_executor
        
        # Задачи в сети
        self.pending_tasks: Dict[str, Dict] = {}
        self.active_tasks: Dict[str, Dict] = {}
        
        # Сетевое взаимодействие
        self.network_tasks = []
        
        # Инициализируем узел в кредитной системе
        self.credit_manager.initialize_node(self.node.node_id)
        
        logger.info(f"🚀 Вычислительная сеть инициализирована на {host}:{port}")
        logger.info(f"🆔 Node ID: {self.node.node_id}")
        self._metrics_app: Optional[web.Application] = None
        self._metrics_runner: Optional[web.AppRunner] = None
    
    def load_config(self, config_file: str) -> Dict:
        """Загружает конфигурацию из файла"""
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Ошибка загрузки конфигурации: {e}")
        
        # Конфигурация по умолчанию
        return {
            "sandbox": {
                "type": "process_isolation",
                "resource_limits": {
                    "cpu_time_seconds": 30,
                    "memory_bytes": 100 * 1024 * 1024,
                    "file_size_bytes": 50 * 1024 * 1024
                }
            },
            "pricing": {
                "base_cpu_price": 0.01,
                "base_gpu_price": 0.05,
                "urgency_multiplier": {
                    "low": 0.8,
                    "normal": 1.0,
                    "high": 1.5,
                    "critical": 2.0
                }
            },
            "reputation": {
                "decay_rate": 0.01,
                "recent_timeframe": 30 * 24 * 3600
            }
        }
    
    def create_pricing_config(self) -> PricingConfig:
        """Создает конфигурацию ценообразования"""
        pricing_config = self.config.get('pricing', {})
        return PricingConfig(
            base_cpu_price=pricing_config.get('base_cpu_price', 0.01),
            base_gpu_price=pricing_config.get('base_gpu_price', 0.05),
            urgency_multiplier=pricing_config.get('urgency_multiplier', {})
        )
    
    def get_sandbox_type(self) -> SandboxType:
        """Получает тип sandbox из конфигурации"""
        sandbox_config = self.config.get('sandbox', {})
        sandbox_type = sandbox_config.get('type', 'process_isolation')
        
        return {
            'wasm': SandboxType.WASM,
            'container': SandboxType.CONTAINER,
            'process_isolation': SandboxType.PROCESS_ISOLATION
        }.get(sandbox_type, SandboxType.PROCESS_ISOLATION)

    def get_sandbox_limits(self) -> SandboxLimits:
        """Создает объект лимитов для песочницы"""
        sandbox_config = self.config.get('sandbox', {})
        limits = sandbox_config.get('resource_limits', {})
        return SandboxLimits(
            cpu_time_seconds=limits.get('cpu_time_seconds', 30),
            memory_bytes=limits.get('memory_bytes', 100 * 1024 * 1024),
            wall_time_seconds=limits.get('wall_time_seconds', sandbox_config.get('wall_time_seconds', 30)),
            file_size_bytes=limits.get('file_size_bytes', 50 * 1024 * 1024),
            open_files=limits.get('open_files', 256),
            working_dir_quota_bytes=limits.get('temp_dir_size', 200 * 1024 * 1024),
            env=limits.get('env', {}),
        )

    async def _run_sandbox_self_test(self):
        """Проверяет работоспособность sandbox на старте"""
        try:
            success = await self.sandbox_executor.run_self_test()
            if not success:
                logger.warning(
                    "Sandbox self-test failed. Tasks will still run, but isolation may be degraded."
                )
        except Exception as exc:
            logger.warning("Sandbox self-test raised an exception: %s", exc)
    
    async def start(self):
        """Запускает сеть"""
        self.running = True
        
        try:
            await self._run_sandbox_self_test()
            # Запускаем сервер узла
            await self.node.start_server()
            # Запускаем метрики
            asyncio.create_task(self._start_metrics_server())
            
            # Запускаем фоновые задачи
            asyncio.create_task(self.task_scheduler())
            asyncio.create_task(self.market_monitor())
            asyncio.create_task(self.reputation_updater())
            asyncio.create_task(self.network_health_checker())
            
            logger.info("✅ Сеть успешно запущена")
            
            # Основной цикл
            while self.running:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("🛑 Получен сигнал выключения")
        except Exception as e:
            logger.error(f"❌ Критическая ошибка: {e}")
        finally:
            await self.stop()
    
    async def stop(self):
        """Останавливает сеть"""
        self.running = False
        
        # Останавливаем узел
        self.node.stop()
        
        # Очищаем sandbox
        try:
            await self.sandbox_executor.close()
        except Exception as e:
            logger.warning(f"Ошибка очистки sandbox: {e}")

        # Останавливаем сервер метрик
        try:
            if self._metrics_runner:
                await self._metrics_runner.cleanup()
        except Exception as e:
            logger.warning(f"Ошибка остановки metrics сервера: {e}")
        
        logger.info("🛑 Сеть остановлена")
    
    async def task_scheduler(self):
        """Планировщик задач"""
        while self.running:
            try:
                # Проверяем pending задачи
                for task_id, task_info in list(self.pending_tasks.items()):
                    await self.assign_task(task_id, task_info)
                
                # Проверяем активные задачи
                for task_id, task_info in list(self.active_tasks.items()):
                    await self.check_task_status(task_id, task_info)
                
                await asyncio.sleep(5)  # Проверяем каждые 5 секунд
                
            except Exception as e:
                logger.error(f"Ошибка в планировщике задач: {e}")
                await asyncio.sleep(10)
    
    async def assign_task(self, task_id: str, task_info: Dict):
        """Назначает задачу подходящему узлу"""
        try:
            task = Task.from_dict(task_info['task'])
            
            # Получаем доступные узлы
            available_nodes = await self.get_available_nodes(task)
            
            if not available_nodes:
                logger.warning(f"Нет доступных узлов для задачи {task_id}")
                return
            
            # Находим оптимальный узел
            optimal_node = self.pricing_engine.get_optimal_node_for_task(
                task.task_type.value,
                task.config.priority.value,
                task.requirements.__dict__,
                available_nodes
            )
            
            if optimal_node:
                # Рассчитываем стоимость
                pricing = self.pricing_engine.calculate_task_price(
                    task.task_type.value,
                    task.config.priority.value,
                    task.requirements.__dict__,
                    optimal_node.get('reputation', 'average'),
                    optimal_node.get('capabilities', {})
                )
                
                # Проверяем баланс владельца
                owner_balance = self.credit_manager.get_balance(task.owner_id)
                if owner_balance >= pricing['total_cost']:
                    # Списываем стоимость
                    self.credit_manager.transfer_credits(
                        task.owner_id, optimal_node['node_id'], 
                        pricing['total_cost'], task_id
                    )
                    
                    # Назначаем задачу
                    task.status = TaskStatus.SCHEDULED
                    self.active_tasks[task_id] = {
                        'task': task,
                        'worker_id': optimal_node['node_id'],
                        'assigned_at': time.time(),
                        'pricing': pricing,
                        'status': TaskStatus.SCHEDULED.value
                    }
                    
                    # Удаляем из pending
                    del self.pending_tasks[task_id]
                    
                    logger.info(f"📝 Задача {task_id} назначена узлу {optimal_node['node_id']}. Стоимость: {pricing['total_cost']}")
                    
                    asyncio.create_task(self._run_local_task(task_id, task))
                else:
                    logger.warning(f"Недостаточно кредитов у владельца задачи {task_id}")
            
        except Exception as e:
            logger.error(f"Ошибка назначения задачи {task_id}: {e}")

    async def _run_local_task(self, task_id: str, task: Task):
        """Запускает выполнение задачи локально с обновлением состояния"""
        try:
            self.active_tasks[task_id]['status'] = TaskStatus.RUNNING.value
            task.status = TaskStatus.RUNNING
            result = await self.task_executor.execute(task)
            self.active_tasks[task_id]['result'] = result
            final_status = result.get('task_status', TaskStatus.COMPLETED.value)
            self.active_tasks[task_id]['status'] = final_status
            if final_status == TaskStatus.COMPLETED.value:
                self.active_tasks[task_id]['completed_at'] = time.time()
            else:
                self.active_tasks[task_id]['error'] = result.get('invalid_results')
            # Репутация: учитываем penalties из верификации
            penalties = result.get('penalties', [])
            for worker_id, reason in penalties:
                await self.reputation_manager.penalize_malicious(worker_id, reason, severity=2.0)
        except Exception as exc:
            logger.error(f"Ошибка выполнения задачи {task_id}: {exc}")
            self.active_tasks[task_id]['status'] = TaskStatus.FAILED.value
            self.active_tasks[task_id]['error'] = str(exc)
    
    async def get_available_nodes(self, task: Task) -> List[Dict]:
        """Получает список доступных узлов для задачи"""
        available_nodes = []
        
        # Здесь должна быть логика получения узлов из сети
        # Пока используем локальные данные
        
        for peer_id, capabilities in self.node.peers.items():
            # Проверяем, может ли узел выполнить задачу
            if self.can_node_execute_task(peer_id, capabilities, task):
                # Получаем репутацию узла
                reputation = await self.reputation_manager.get_reputation_level(peer_id)
                
                available_nodes.append({
                    'node_id': peer_id,
                    'capabilities': capabilities,
                    'reputation': reputation
                })
        
        return available_nodes
    
    def can_node_execute_task(self, node_id: str, capabilities: Dict, task: Task) -> bool:
        """Проверяет, может ли узел выполнить задачу"""
        # Проверяем тип задачи
        if task.task_type not in [TaskType.RANGE_REDUCE, TaskType.MAP, TaskType.MAP_REDUCE,
                                 TaskType.MATRIX_OPS, TaskType.ML_INFERENCE, TaskType.ML_TRAIN_STEP]:
            return False
        
        # Проверяем требования к ресурсам
        if task.requirements.cpu_percent > 95:
            return False
        
        if task.requirements.ram_gb > capabilities.ram_gb:
            return False
        
        if task.requirements.gpu_percent > 0 and capabilities.gpu_score == 0:
            return False
        
        # Проверяем загрузку
        cpu_load = capabilities.cpu_usage
        gpu_load = capabilities.gpu_usage
        
        if cpu_load > 90 or gpu_load > 90:
            return False
        
        return True
    
    async def check_task_status(self, task_id: str, task_info: Dict):
        """Проверяет статус активной задачи"""
        try:
            task = task_info['task']
            worker_id = task_info['worker_id']
            
            # Здесь должна быть логика проверки статуса задачи в сети
            # Пока имитируем проверку
            
            # Если задача выполняется более 5 минут, считаем ее зависшей
            if time.time() - task_info['assigned_at'] > 300:
                logger.warning(f"Задача {task_id} выполняется слишком долго")
                
                # Отменяем задачу
                await self.cancel_task(task_id, "Timeout")
            
        except Exception as e:
            logger.error(f"Ошибка проверки статуса задачи {task_id}: {e}")
    
    async def notify_task_assignment(self, task_id: str, worker_id: str):
        """Уведомляет узел о назначении задачи"""
        # Отправляем уведомление в сеть
        await self.node.send_message(
            {'type': 'task_assignment_notification', 'task_id': task_id},
            worker_id
        )
        logger.info(f"📤 Уведомление о назначении задачи {task_id} узлу {worker_id}")
    
    async def cancel_task(self, task_id: str, reason: str):
        """Отменяет задачу"""
        if task_id in self.active_tasks:
            task_info = self.active_tasks[task_id]
            
            # Возвращаем кредиты владельцу
            pricing = task_info.get('pricing')
            if pricing:
                self.credit_manager.transfer_credits(
                    task_info['worker_id'], task_info['task'].owner_id,
                    pricing['total_cost'], task_id
                )
            
            # Штрафуем воркера
            await self.reputation_manager.penalize_malicious(
                task_info['worker_id'], f"Task cancellation: {reason}"
            )
            
            # Уведомляем воркера об отмене
            await self.node.send_message(
                {'type': 'task_cancellation', 'task_id': task_id, 'reason': reason},
                task_info['worker_id']
            )

            # Удаляем из активных
            del self.active_tasks[task_id]
            
            logger.info(f"❌ Задача {task_id} отменена: {reason}")
    
    async def market_monitor(self):
        """Мониторит рыночные условия"""
        while self.running:
            try:
                # Собираем метрики сети
                metrics = self.collect_network_metrics()
                
                # Обновляем ценообразование
                self.pricing_engine.update_market_metrics(metrics)
                
                await asyncio.sleep(30)  # Мониторинг каждые 30 секунд
                
            except Exception as e:
                logger.error(f"Ошибка в мониторе рынка: {e}")
                await asyncio.sleep(60)
    
    def collect_network_metrics(self) -> ResourceMetrics:
        """Собирает метрики сети"""
        # Рассчитываем среднюю загрузку по сети
        total_cpu = 0
        total_gpu = 0
        total_ram = 0
        total_nodes = len(self.node.peers)
        
        # Получаем метрики текущего узла
        current_cpu = self.node.capabilities.cpu_usage
        current_gpu = self.node.capabilities.gpu_usage
        current_ram = self.node.capabilities.ram_usage
        
        # Инициализируем средние значения текущими метриками
        avg_cpu = current_cpu
        avg_gpu = current_gpu
        avg_ram = current_ram

        # Если есть пиры, добавляем их метрики
        if total_nodes > 0:
            for capabilities in self.node.peers.values():
                total_cpu += capabilities.cpu_usage
                total_gpu += capabilities.gpu_usage
                total_ram += capabilities.ram_usage
            
            # Включаем текущий узел в расчеты
            total_cpu += current_cpu
            total_gpu += current_gpu
            total_ram += current_ram
            
            total_nodes += 1
            
            avg_cpu = total_cpu / total_nodes
            avg_gpu = total_gpu / total_nodes
            avg_ram = total_ram / total_nodes
        
        return ResourceMetrics(
            cpu_usage=avg_cpu,
            gpu_usage=avg_gpu,
            ram_usage=avg_ram,
            disk_usage=0,
            active_tasks=len(self.active_tasks),
            available_nodes=total_nodes
        )
    
    async def reputation_updater(self):
        """Обновляет репутацию"""
        while self.running:
            try:
                # Обновляем репутацию всех узлов
                for node_id in self.node.peers:
                    await self.reputation_manager.get_reputation_score(node_id)
                
                await asyncio.sleep(60)  # Обновляем каждую минуту
                
            except Exception as e:
                logger.error(f"Ошибка в обновлении репутации: {e}")
                await asyncio.sleep(120)
    
    async def network_health_checker(self):
        """Проверяет здоровье сети"""
        while self.running:
            try:
                # Проверяем здоровье кредитной системы
                credit_health = self.credit_manager.get_network_health()
                logger.info(f"💳 Здоровье кредитной системы: {credit_health}")
                
                # Проверяем статистику репутации
                rep_stats = await self.reputation_manager.get_network_reputation_stats()
                logger.info(f"📊 Статистика репутации: {rep_stats}")
                
                # Проверяем ценообразование
                pricing_analytics = self.pricing_engine.get_pricing_analytics()
                logger.info(f"💰 Аналитика ценообразования: {pricing_analytics.get('market_condition', 'unknown')}")
                
                await asyncio.sleep(300)  # Проверяем каждые 5 минут
                
            except Exception as e:
                logger.error(f"Ошибка в проверке здоровья сети: {e}")
                await asyncio.sleep(600)
    
    # API методы
    async def submit_task(self, task_data: Dict) -> str:
        """Подает задачу в сеть"""
        try:
            # Создаем задачу
            task = Task.from_dict(task_data)
            
            # Валидируем задачу
            errors = task.validate()
            if errors:
                raise ValueError(f"Ошибка валидации задачи: {errors}")
            
        # Генерируем ID задачи
        task_id = task.task_id
        
        # Добавляем в pending задачи
        self.pending_tasks[task_id] = {
            'task': task.to_dict(),
            'submitted_at': time.time(),
            'status': TaskStatus.PENDING.value
        }
            
            logger.info(f"📝 Задача {task_id} подана в сеть")
            return task_id
            
        except Exception as e:
            logger.error(f"Ошибка подачи задачи: {e}")
            raise
    
    async def get_task_status(self, task_id: str) -> Dict:
        """Получает статус задачи"""
        if task_id in self.pending_tasks:
            return {
                'task_id': task_id,
                'status': self.pending_tasks[task_id]['status'],
                'submitted_at': self.pending_tasks[task_id]['submitted_at']
            }
        
        elif task_id in self.active_tasks:
            task_info = self.active_tasks[task_id]
            return {
                'task_id': task_id,
                'status': task_info['status'],
                'worker_id': task_info['worker_id'],
                'assigned_at': task_info['assigned_at'],
                'pricing': task_info.get('pricing', {}),
                'result': task_info.get('result'),
                'completed_at': task_info.get('completed_at'),
                'error': task_info.get('error')
            }
        
        else:
            return {'task_id': task_id, 'status': 'not_found'}
    
    async def get_network_status(self) -> Dict:
        """Получает статус сети"""
        job_counters = {}
        if hasattr(self.node, "scheduler_state"):
            counters = self.node.scheduler_state.status_counters()
            job_counters = {status.value if hasattr(status, "value") else str(status): count for status, count in counters.items()}
        avg_job_latency = 0.0
        if getattr(self.node, "_job_latencies", None):
            latencies = [x for x in self.node._job_latencies if x is not None]
            if latencies:
                avg_job_latency = sum(latencies) / len(latencies)

        return {
            'node_id': self.node.node_id,
            'host': self.node.host,
            'port': self.node.port,
            'peers_count': len(self.node.peers),
            'pending_tasks': len(self.pending_tasks),
            'active_tasks': len(self.active_tasks),
            'credits': float(self.credit_manager.get_balance(self.node.node_id)),
            'reputation_score': await self.reputation_manager.get_reputation_score(self.node.node_id),
            'pricing_analytics': self.pricing_engine.get_pricing_analytics(),
            'cpu_usage': self.node.capabilities.cpu_usage,
            'ram_usage': self.node.capabilities.ram_usage,
            'job_statuses': job_counters,
            'avg_job_latency_sec': avg_job_latency,
            'job_events': self.node.event_log[-50:],  # последние события
            'scheduler_events': self.node.scheduler_state.to_event_list(),
        }

    async def _metrics_handler(self, request):
        status = await self.get_network_status()
        return web.json_response(status)

    async def _metrics_prometheus_handler(self, request):
        """Простой экспорт в формате Prometheus text."""
        status = await self.get_network_status()
        lines = []
        for key, val in status.items():
            if isinstance(val, dict):
                for subk, subv in val.items():
                    metric_name = f"wf_{key}_{subk}".replace(".", "_")
                    lines.append(f"# TYPE {metric_name} gauge")
                    lines.append(f'{metric_name} {subv}')
            else:
                metric_name = f"wf_{key}".replace(".", "_")
                lines.append(f"# TYPE {metric_name} gauge")
                lines.append(f'{metric_name} {val}')
        text = "\n".join(lines) + "\n"
        return web.Response(text=text, content_type="text/plain")

    async def _start_metrics_server(self):
        """Запускает простой HTTP endpoint /metrics на порту port+100"""
        try:
            self._metrics_app = web.Application()
            self._metrics_app.router.add_get("/metrics", self._metrics_handler)
            self._metrics_app.router.add_get("/metrics_prom", self._metrics_prometheus_handler)
            self._metrics_runner = web.AppRunner(self._metrics_app)
            await self._metrics_runner.setup()
            site = web.TCPSite(self._metrics_runner, self.host, self.port + 100)
            await site.start()
            logger.info("📊 Metrics endpoint запущен на %s:%s/metrics", self.host, self.port + 100)
        except Exception as exc:
            logger.warning("Не удалось запустить metrics endpoint: %s", exc)

def signal_handler(signum, frame):
    """Обработчик сигналов"""
    logger.info(f"Получен сигнал {signum}, завершение работы...")
    sys.exit(0)

def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(description='Децентрализованная вычислительная сеть')
    parser.add_argument('--host', default='0.0.0.0', help='Хост для прослушивания')
    parser.add_argument('--port', type=int, default=5555, help='Порт для прослушивания')
    parser.add_argument('--config', help='Файл конфигурации')
    parser.add_argument('--sandbox', choices=['wasm', 'container', 'process_isolation'], 
                       default='process_isolation', help='Тип sandbox')
    parser.add_argument('--debug', action='store_true', help='Режим отладки')
    
    args = parser.parse_args()
    
    # Устанавливаем обработчик сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Устанавливаем уровень логирования
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Создаем и запускаем сеть
        network = ComputeNetwork(args.host, args.port, args.config)
        
        # Запускаем
        asyncio.run(network.start())
        
    except Exception as e:
        logger.error(f"Ошибка запуска: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
