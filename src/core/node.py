#!/usr/bin/env python3
"""
Основной класс узла для децентрализованной вычислительной сети
"""

import asyncio
import json
import time
import socket
import threading
import uuid
import hashlib
import base64
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor
import psutil

try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False
    print("⚠️ GPUtil not available, GPU features disabled")

@dataclass
class NodeCapability:
    """Возможности узла"""
    node_id: str
    cpu_score: int
    gpu_score: int
    ram_gb: int
    max_parallel_tasks: int
    min_price: Dict[str, float]
    gpu_name: Optional[str] = None
    cpu_cores: int = 0
    disk_gb: int = 0
    # Текущая загрузка
    cpu_usage: float = 0.0
    gpu_usage: float = 0.0
    ram_usage: float = 0.0
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_node(cls, node_id: str):
        """Создает capabilities на основе текущей системы"""
        # Получаем информацию о системе
        cpu_info = psutil.cpu_freq()
        cpu_cores = psutil.cpu_count()
        ram_gb = round(psutil.virtual_memory().total / (1024**3), 2)
        disk_gb = round(psutil.disk_usage('/').total / (1024**3), 2)
        
        # GPU информация
        gpu_score = 0
        gpu_name = None
        
        if GPU_AVAILABLE:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    # Используем самый мощный GPU
                    best_gpu = max(gpus, key=lambda g: g.memoryTotal)
                    gpu_score = int(best_gpu.memoryTotal)  # в МБ
                    gpu_name = best_gpu.name
            except Exception:
                # Если не удалось получить GPU информацию, отключаем GPU
                pass
        
        # CPU score основан на частоте и ядрах
        cpu_score = int(cpu_info.current * cpu_cores / 1000) if cpu_info else cpu_cores
        
        # Получаем текущую загрузку
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        
        gpu_usage = 0.0
        if GPU_AVAILABLE and gpu_score > 0:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu_usage = gpus[0].load * 100  # в процентах
            except Exception:
                pass
        
        return cls(
            node_id=node_id,
            cpu_score=cpu_score,
            gpu_score=gpu_score,
            ram_gb=ram_gb,
            max_parallel_tasks=max(1, cpu_cores // 2),
            min_price={"cpu": 0.01, "gpu": 0.05},  # базовые цены
            gpu_name=gpu_name,
            cpu_cores=cpu_cores,
            disk_gb=disk_gb,
            cpu_usage=cpu_usage,
            gpu_usage=gpu_usage,
            ram_usage=ram_usage
        )

class ComputeNode:
    """Основной класс узла для вычислительной сети"""
    
    def __init__(self, host: str = '0.0.0.0', port: int = 5555):
        self.host = host
        self.port = port
        self.node_id = self.generate_node_id()
        self.capabilities = NodeCapability.from_node(self.node_id)
        
        # Состояние сети
        self.peers: Dict[str, Dict] = {}  # peer_id -> capabilities
        self.tasks: Dict[str, Dict] = {}  # task_id -> task_info
        self.reputation = {"successful_tasks": 0, "failed_tasks": 0, "penalties": 0}
        
        # Compute credits
        self.credits = 0.0
        self.credit_history: List[Dict] = []
        
        # Сетевое взаимодействие
        self.server = None # Для asyncio сервера
        self.server_socket = None # Для старой реализации
        self.running = False
        self.message_handlers = {}
        
        # Пул для выполнения задач
        self.task_executor = ThreadPoolExecutor(max_workers=self.capabilities.max_parallel_tasks)
        
        # Регистрируем обработчики сообщений
        self.register_message_handlers()
    
    def generate_node_id(self) -> str:
        """Генерирует уникальный ID узла"""
        unique_string = f"{self.host}:{self.port}:{uuid.uuid4()}"
        return hashlib.sha256(unique_string.encode()).hexdigest()[:32]
    
    def register_message_handlers(self):
        """Регистрирует обработчики сообщений"""
        self.message_handlers = {
            'capability_exchange': self.handle_capability_exchange,
            'task_request': self.handle_task_request,
            'task_result': self.handle_task_result,
            'credit_transfer': self.handle_credit_transfer,
            'peer_discovery': self.handle_peer_discovery,
            'reputation_query': self.handle_reputation_query,
            'task_assignment': self.handle_task_assignment,  # Добавляем новый обработчик
            'task_cancellation': self.handle_task_cancellation # Добавляем новый обработчик
        }
    
    async def start_server(self):
        """Запускает сервер для приема подключений"""
        # Запускаем сервер asyncio
        self.server = await asyncio.start_server(
            self.handle_client_connection, self.host, self.port
        )
        
        self.running = True
        
        print(f"🚀 Вычислительный узел запущен на {self.host}:{self.port}")
        print(f"🆔 Node ID: {self.node_id}")
        print(f"💪 Возможности: CPU={self.capabilities.cpu_score}, GPU={self.capabilities.gpu_score}, RAM={self.capabilities.ram_gb}GB")
        
        # Запускаем периодическое обновление состояния
        asyncio.create_task(self.periodic_update())
    
    async def handle_client_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Обрабатывает подключение конкретного клиента"""
        addr = writer.get_extra_info('peername')
        peer_address = f"{addr[0]}:{addr[1]}"
        
        print(f"🔗 Подключен новый пир: {peer_address}")
        
        try:
            while True:
                data = await reader.read(4096)
                if not data:
                    break
                
                try:
                    message = json.loads(data.decode('utf-8'))
                    await self.process_message(message, peer_address)
                except json.JSONDecodeError:
                    print(f"⚠️ Некорректное сообщение от {peer_address}")
                    
        except Exception as e:
            print(f"❌ Ошибка обработки клиента {peer_address}: {e}")
        finally:
            print(f"🔌 Отключен пир: {peer_address}")
            self.remove_peer(peer_address)
            writer.close()
            await writer.wait_closed()
    
    async def process_message(self, message: Dict, peer_address: str):
        """Обрабатывает полученное сообщение"""
        msg_type = message.get('type')
        handler = self.message_handlers.get(msg_type)
        
        if handler:
            try:
                await handler(message, peer_address)
            except Exception as e:
                print(f"❌ Ошибка обработки сообщения {msg_type}: {e}")
        else:
            print(f"⚠️ Неизвестный тип сообщения: {msg_type}")
    
    async def handle_capability_exchange(self, message: Dict, peer_address: str):
        """Обмен возможностями между узлами"""
        capabilities_data = message.get('capabilities')
        if capabilities_data:
            self.peers[peer_address] = capabilities_data
            print(f"📦 Получены возможности от {peer_address}: CPU={capabilities_data.get('cpu_score', 0)}")
            
            # Отправляем свои возможности в ответ
            response = {
                'type': 'capability_exchange',
                'capabilities': self.capabilities.to_dict()
            }
            await self.send_message(response, peer_address)
    
    async def handle_task_request(self, message: Dict, peer_address: str):
        """Обработка запроса на выполнение задачи"""
        task = message.get('task')
        if task and self.can_execute_task(task):
            task_id = task.get('task_id')
            
            # Принимаем задачу
            self.tasks[task_id] = {
                'task': task,
                'status': 'accepted',
                'worker_id': peer_address,
                'started_at': time.time()
            }
            
            print(f"📝 Принята задача {task_id} от {peer_address}")
            
            # Выполняем задачу
            self.task_executor.submit(self.execute_task, task_id, task)
            
            # Отправляем подтверждение
            response = {
                'type': 'task_accepted',
                'task_id': task_id,
                'worker_id': self.node_id
            }
            await self.send_message(response, peer_address)
    
    async def handle_task_result(self, message: Dict, peer_address: str):
        """Обработка результата выполнения задачи"""
        task_id = message.get('task_id')
        result = message.get('result')
        success = message.get('success', False)
        
        if task_id in self.tasks:
            self.tasks[task_id]['status'] = 'completed' if success else 'failed'
            self.tasks[task_id]['result'] = result
            self.tasks[task_id]['completed_at'] = time.time()
            
            print(f"✅ Задача {task_id} завершена: {'успешно' if success else 'неудачно'}")
            
            # Обновляем репутацию
            if success:
                self.reputation['successful_tasks'] += 1
            else:
                self.reputation['failed_tasks'] += 1
                self.reputation['penalties'] += 1
    
    async def handle_credit_transfer(self, message: Dict, peer_address: str):
        """Обработка перевода compute-кредитов"""
        amount = message.get('amount', 0)
        from_id = message.get('from_id')
        to_id = message.get('to_id')
        
        if from_id == self.node_id:
            self.credits -= amount
            print(f"💸 Списано {amount} compute-кредитов")
        elif to_id == self.node_id:
            self.credits += amount
            print(f"💸 Начислено {amount} compute-кредитов")
        
        # Записываем в историю
        self.credit_history.append({
            'timestamp': time.time(),
            'from_id': from_id,
            'to_id': to_id,
            'amount': amount,
            'balance_after': self.credits
        })
    
    async def handle_peer_discovery(self, message: Dict, peer_address: str):
        """Обнаружение других узлов в сети"""
        known_peers = message.get('peers', [])
        
        for peer_info in known_peers:
            peer_addr = peer_info.get('address')
            if peer_addr and peer_addr != f"{self.host}:{self.port}":
                if peer_addr not in self.peers:
                    print(f"🔍 Обнаружен новый узел: {peer_addr}")
                    # TODO: Реализовать подключение к новому узлу
    
    async def handle_reputation_query(self, message: Dict, peer_address: str):
        """Запрос репутации узла"""
        query_node_id = message.get('node_id')
        
        if query_node_id == self.node_id:
            # Отправляем свою репутацию
            response = {
                'type': 'reputation_response',
                'node_id': self.node_id,
                'reputation': self.reputation
            }
            await self.send_message(response, peer_address)
    
    async def handle_task_assignment(self, message: Dict, peer_address: str):
        """Обработка назначения задачи от координатора"""
        task_id = message.get('task_id')
        task_info = message.get('task_info')
        
        if task_id and task_info:
            self.tasks[task_id] = {
                'task': task_info['task'],
                'status': 'assigned',
                'worker_id': self.node_id,
                'assigned_at': time.time()
            }
            print(f"📝 Получено назначение задачи {task_id} от {peer_address}")
            
            # Запускаем выполнение задачи в пуле
            self.task_executor.submit(self.execute_task, task_id, task_info['task'])
    
    async def handle_task_cancellation(self, message: Dict, peer_address: str):
        """Обработка отмены задачи"""
        task_id = message.get('task_id')
        reason = message.get('reason', 'Unknown reason')
        
        if task_id in self.tasks:
            self.tasks[task_id]['status'] = 'cancelled'
            print(f"❌ Задача {task_id} отменена пиром {peer_address}. Причина: {reason}")
            # Здесь можно добавить логику для остановки выполнения задачи, если она активна
    
    def can_execute_task(self, task: Dict) -> bool:
        """Проверяет, может ли узел выполнить задачу"""
        task_type = task.get('type')
        requirements = task.get('requirements', {})
        
        # Проверяем типы задач (только разрешенные)
        allowed_types = ['range_reduce', 'map', 'map_reduce', 'matrix_ops', 'ml_inference', 'ml_train_step']
        if task_type not in allowed_types:
            return False
        
        # Проверяем требования к ресурсам
        if requirements.get('cpu_percent', 0) > 95:
            return False
        
        if requirements.get('ram_gb', 0) > self.capabilities.ram_gb:
            return False
        
        if requirements.get('gpu_percent', 0) > 0 and self.capabilities.gpu_score == 0:
            return False
        
        # Проверяем цену
        max_price = task.get('max_price', 0)
        min_price = self.get_task_price(task_type)
        
        return max_price >= min_price
    
    def get_task_price(self, task_type: str) -> float:
        """Получает минимальную цену для типа задачи"""
        base_prices = {
            'range_reduce': 0.01,
            'map': 0.02,
            'map_reduce': 0.05,
            'matrix_ops': 0.03,
            'ml_inference': 0.1,
            'ml_train_step': 0.2
        }
        return base_prices.get(task_type, 0.01)
    
    def execute_task(self, task_id: str, task: Dict):
        """Выполняет задачу в sandbox"""
        try:
            print(f"🔄 Выполнение задачи {task_id}")
            
            # Здесь будет реальное выполнение в sandbox
            # Пока имитируем выполнение
            time.sleep(2)  # Имитация вычислений
            
            # Генерируем результат
            result = {
                'task_id': task_id,
                'result_data': f"Результат для задачи {task_id}",
                'execution_time': 2.0,
                'resource_used': {
                    'cpu_percent': 50,
                    'ram_gb': 1.0,
                    'gpu_percent': 0
                }
            }
            
            # Отправляем результат
            response = {
                'type': 'task_result',
                'task_id': task_id,
                'result': result,
                'success': True
            }
            
            # Шлем результат координатору (здесь упрощено)
            asyncio.run(self.broadcast_message(response))
            
        except Exception as e:
            print(f"❌ Ошибка выполнения задачи {task_id}: {e}")
            
            # Отправляем об ошибке
            response = {
                'type': 'task_result',
                'task_id': task_id,
                'result': {'error': str(e)},
                'success': False
            }
            asyncio.run(self.broadcast_message(response))
    
    async def send_message(self, message: Dict, target_peer_address: str):
        """Отправляет сообщение указанному пиру"""
        try:
            host, port_str = target_peer_address.split(':')
            port = int(port_str)
            
            reader, writer = await asyncio.open_connection(host, port)
            
            # Добавляем подпись к сообщению
            message['timestamp'] = time.time()
            message['from_node_id'] = self.node_id
            message_json = json.dumps(message)
            
            writer.write(message_json.encode('utf-8'))
            await writer.drain()
            
            writer.close()
            await writer.wait_closed()
            
            # print(f"✅ Сообщение отправлено {target_peer_address}: {message['type']}")
            
        except ConnectionRefusedError:
            print(f"❌ Соединение отклонено пиром {target_peer_address}")
            # Удаляем недоступный пир
            self.remove_peer(target_peer_address)
        except Exception as e:
            print(f"❌ Ошибка отправки сообщения {target_peer_address}: {e}")
    
    async def broadcast_message(self, message: Dict):
        """Отправляет сообщение всем известным пирам"""
        # Создаем список задач для параллельной отправки
        send_tasks = [
            self.send_message(message, peer_address)
            for peer_address in self.peers.keys()
        ]
        
        # Ждем завершения всех задач
        await asyncio.gather(*send_tasks, return_exceptions=True)
    
    def remove_peer(self, peer_address: str):
        """Удаляет пира из списка"""
        if peer_address in self.peers:
            del self.peers[peer_address]
            print(f"🔌 Отключен узел: {peer_address}")
    
    async def periodic_update(self):
        """Периодическое обновление состояния узла"""
        while self.running:
            # Обновляем capabilities
            self.capabilities = NodeCapability.from_node(self.node_id)
            
            # Обмен возможностями с пирами
            if self.peers:
                message = {
                    'type': 'capability_exchange',
                    'capabilities': self.capabilities.to_dict()
                }
                await self.broadcast_message(message)
            
            # Ждем 30 секунд
            await asyncio.sleep(30)
    
    def get_status(self) -> Dict:
        """Получает текущее состояние узла"""
        return {
            'node_id': self.node_id,
            'host': self.host,
            'port': self.port,
            'capabilities': self.capabilities.to_dict(),
            'peers_count': len(self.peers),
            'active_tasks': len([t for t in self.tasks.values() if t['status'] == 'accepted']),
            'credits': self.credits,
            'reputation': self.reputation
        }
    
    def stop(self):
        """Останавливает работу узла"""
        self.running = False
        if self.server:
            self.server.close()
            # await self.server.wait_closed() # Это вызовет ошибку, если сервер уже закрыт
        self.task_executor.shutdown(wait=True)
        print("🛑 Вычислительный узел остановлен")

if __name__ == "__main__":
    # Пример использования
    node = ComputeNode()
    print(f"Создан узел с ID: {node.node_id}")
    print(f"Возможности: {node.capabilities}")