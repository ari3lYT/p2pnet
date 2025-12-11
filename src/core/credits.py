#!/usr/bin/env python3
"""
Система compute-кредитов для децентрализованной вычислительной сети
"""

import threading
import time
from dataclasses import asdict, dataclass
from decimal import Decimal, getcontext
from enum import Enum
from typing import Dict, List, Optional, Tuple


class CreditEventType(Enum):
    """Типы событий кредитов"""
    TASK_EXECUTION = "task_execution"
    CREDIT_TRANSFER = "credit_transfer"
    REWARD = "reward"
    PENALTY = "penalty"
    REFUND = "refund"

@dataclass
class CreditEvent:
    """Событие кредитной системы"""
    event_id: str
    event_type: CreditEventType
    timestamp: float
    from_node: str
    to_node: str
    amount: Decimal
    task_id: Optional[str] = None
    description: Optional[str] = None
    
    def to_dict(self) -> Dict:
        result = asdict(self)
        result['event_type'] = self.event_type.value
        result['amount'] = float(self.amount)
        return {k: v for k, v in result.items() if v is not None}

class CreditManager:
    """Менеджер compute-кредитов"""
    
    def __init__(self):
        # Точность вычислений
        getcontext().prec = 10
        
        # Балансы узлов
        self.balances: Dict[str, Decimal] = {}
        
        # История событий
        self.events: List[CreditEvent] = []
        
        # Блокировки для потокобезопасности
        self.lock = threading.RLock()
        
        # Курсы конвертации ресурсов
        self.resource_rates = {
            'cpu_second': Decimal('0.01'),    # 1 CPU-секунда = 0.01 кредита
            'gpu_second': Decimal('0.05'),    # 1 GPU-секунда = 0.05 кредита
            'ram_gb_hour': Decimal('0.02'),   # 1 GB RAM в час = 0.02 кредита
            'disk_gb_hour': Decimal('0.005'), # 1 GB диска в час = 0.005 кредита
        }
        
        # Множители для типов задач
        self.task_type_multipliers = {
            'range_reduce': Decimal('1.0'),
            'map': Decimal('1.2'),
            'map_reduce': Decimal('1.5'),
            'matrix_ops': Decimal('1.3'),
            'ml_inference': Decimal('2.0'),
            'ml_train_step': Decimal('3.0'),
        }
        
        # Множители для приоритетов
        self.priority_multipliers = {
            'low': Decimal('0.8'),
            'normal': Decimal('1.0'),
            'high': Decimal('1.5'),
        }
    
    def initialize_node(self, node_id: str, initial_credits: Decimal = Decimal('0')):
        """Инициализирует узел в системе кредитов"""
        with self.lock:
            if node_id not in self.balances:
                self.balances[node_id] = initial_credits
                print(f"🆔 Узел {node_id} инициализирован с {initial_credits} кредитов")
    
    def get_balance(self, node_id: str) -> Decimal:
        """Получает баланс узла"""
        with self.lock:
            return self.balances.get(node_id, Decimal('0'))
    
    def add_credits(self, node_id: str, amount: Decimal, description: str = "") -> bool:
        """Добавляет кредиты узлу"""
        with self.lock:
            if node_id not in self.balances:
                self.balances[node_id] = Decimal('0')
            
            old_balance = self.balances[node_id]
            self.balances[node_id] += amount
            
            # Записываем событие
            event = CreditEvent(
                event_id=str(int(time.time() * 1000000)),
                event_type=CreditEventType.REWARD,
                timestamp=time.time(),
                from_node="system",
                to_node=node_id,
                amount=amount,
                description=description
            )
            self.events.append(event)
            
            print(f"💸 Начислено {amount} кредитов узлу {node_id}. Баланс: {self.balances[node_id]}")
            return True
    
    def transfer_credits(self, from_node: str, to_node: str, amount: Decimal, task_id: Optional[str] = None) -> bool:
        """Переводит кредиты между узлами"""
        with self.lock:
            # Проверяем баланс отправителя
            if from_node not in self.balances:
                self.balances[from_node] = Decimal('0')
            
            if self.balances[from_node] < amount:
                print(f"❌ Недостаточно кредитов у {from_node}. Требуется: {amount}, имеется: {self.balances[from_node]}")
                return False
            
            # Проверяем получателя
            if to_node not in self.balances:
                self.balances[to_node] = Decimal('0')
            
            # Выполняем перевод
            self.balances[from_node] -= amount
            self.balances[to_node] += Decimal(str(amount))
            
            # Записываем событие
            event = CreditEvent(
                event_id=str(int(time.time() * 1000000)),
                event_type=CreditEventType.CREDIT_TRANSFER,
                timestamp=time.time(),
                from_node=from_node,
                to_node=to_node,
                amount=amount,
                task_id=task_id,
                description="Перевод кредитов за выполнение задачи"
            )
            self.events.append(event)
            
            print(f"💸 Перевод {amount} кредитов с {from_node} на {to_node}")
            return True
    
    def calculate_task_cost(self, task_type: str, priority: str, resource_usage: Dict, node_capabilities: Dict) -> Decimal:
        """Рассчитывает стоимость задачи на основе использования ресурсов"""
        cost = Decimal('0')
        
        # Базовая стоимость CPU
        cpu_seconds = resource_usage.get('cpu_seconds', 0)
        if cpu_seconds > 0:
            cpu_cost = cpu_seconds * self.resource_rates['cpu_second']
            cost += cpu_cost
        
        # Базовая стоимость GPU
        gpu_seconds = resource_usage.get('gpu_seconds', 0)
        if gpu_seconds > 0:
            gpu_cost = gpu_seconds * self.resource_rates['gpu_second']
            cost += gpu_cost
        
        # Базовая стоимость RAM
        ram_gb_hours = resource_usage.get('ram_gb_hours', 0)
        if ram_gb_hours > 0:
            ram_cost = ram_gb_hours * self.resource_rates['ram_gb_hour']
            cost += ram_cost
        
        # Базовая стоимость диска
        disk_gb_hours = resource_usage.get('disk_gb_hours', 0)
        if disk_gb_hours > 0:
            disk_cost = disk_gb_hours * self.resource_rates['disk_gb_hour']
            cost += disk_cost
        
        # Применяем множитель типа задачи
        task_multiplier = self.task_type_multipliers.get(task_type, Decimal('1.0'))
        cost *= task_multiplier
        
        # Применяем множитель приоритета
        priority_multiplier = self.priority_multipliers.get(priority, Decimal('1.0'))
        cost *= priority_multiplier
        
        # Учитываем нагрузку на узле (чем выше нагрузка, тем дороже)
        cpu_load = node_capabilities.get('cpu_score', 100) / 100.0
        gpu_load = node_capabilities.get('gpu_score', 0) / 100.0 if node_capabilities.get('gpu_score', 0) > 0 else 1.0
        
        load_multiplier = Decimal(str(1.0 + (cpu_load + gpu_load) / 4.0))
        cost *= load_multiplier
        
        # Округляем до 4 знаков после запятой
        return cost.quantize(Decimal('0.0001'))
    
    def process_task_execution(self, task_id: str, owner_id: str, worker_id: str, 
                             task_type: str, priority: str, resource_usage: Dict, 
                             node_capabilities: Dict, success: bool = True) -> Tuple[bool, Decimal]:
        """Обрабатывает выполнение задачи и списание/начисление кредитов"""
        
        # Если воркер - это владелец задачи, ничего не меняем
        if worker_id == owner_id:
            return True, Decimal('0')
        
        # Рассчитываем стоимость
        if success:
            cost = self.calculate_task_cost(task_type, priority, resource_usage, node_capabilities)
            
            # Списываем с владельца задачи
            if not self.transfer_credits(owner_id, worker_id, cost, task_id):
                print(f"❌ Не удалось списать {cost} кредитов с {owner_id} для задачи {task_id}")
                return False, cost
            
            print(f"✅ Задача {task_id} выполнена успешно. Стоимость: {cost} кредитов")
            return True, cost
        else:
            # Задача не выполнена, возвращаем кредиты владельцу
            # Сначала рассчитываем, сколько было потрачено
            estimated_cost = self.calculate_task_cost(task_type, priority, resource_usage, node_capabilities)
            
            # Возвращаем часть кредитов (50% от оценочной стоимости)
            refund_amount = estimated_cost * Decimal('0.5')
            
            if refund_amount > 0:
                self.transfer_credits(worker_id, owner_id, refund_amount, task_id)
                print(f"⚠️ Задача {task_id} выполнена с ошибкой. Возвращено {refund_amount} кредитов")
            
            return False, refund_amount
    
    def apply_penalty(self, node_id: str, amount: Decimal, reason: str) -> bool:
        """Применяет штраф к узлу"""
        with self.lock:
            if node_id not in self.balances:
                self.balances[node_id] = Decimal('0')
            
            if self.balances[node_id] < amount:
                amount = self.balances[node_id]  # Штраф не может превышать баланс
            
            self.balances[node_id] -= amount
            
            # Записываем событие
            event = CreditEvent(
                event_id=str(int(time.time() * 1000000)),
                event_type=CreditEventType.PENALTY,
                timestamp=time.time(),
                from_node=node_id,
                to_node="system",
                amount=amount,
                description=f"Штраф: {reason}"
            )
            self.events.append(event)
            
            print(f"💸 Штраф {amount} кредитов узлу {node_id}. Причина: {reason}")
            return True
    
    def reward_node(self, node_id: str, amount: Decimal, reason: str) -> bool:
        """Награждает узла"""
        return self.add_credits(node_id, amount, reason)
    
    def get_transaction_history(self, node_id: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """Получает историю транзакций"""
        with self.lock:
            if node_id:
                # Фильтруем по узлу
                filtered_events = [
                    event.to_dict() for event in self.events
                    if event.from_node == node_id or event.to_node == node_id
                ]
            else:
                # Все события
                filtered_events = [event.to_dict() for event in self.events]
            
            # Сортируем по времени (новые primero)
            filtered_events.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return filtered_events[:limit]
    
    def get_credit_statistics(self) -> Dict:
        """Получает статистику кредитной системы"""
        with self.lock:
            total_credits = sum(self.balances.values()) if self.balances else Decimal('0')
            total_nodes = len(self.balances)
            total_transactions = len(self.events)
            
            # Статистика по типам событий
            event_types = {}
            for event in self.events:
                event_type = event.event_type.value
                event_types[event_type] = event_types.get(event_type, 0) + 1
            
            return {
                'total_credits': float(total_credits),
                'total_nodes': total_nodes,
                'total_transactions': total_transactions,
                'event_types': event_types,
                'average_balance': float(total_credits / total_nodes) if total_nodes > 0 else 0
            }
    
    def export_credits_data(self) -> Dict:
        """Экспортирует все данные кредитной системы"""
        with self.lock:
            return {
                'balances': {node_id: float(balance) for node_id, balance in self.balances.items()},
                'events': [event.to_dict() for event in self.events],
                'resource_rates': {k: float(v) for k, v in self.resource_rates.items()},
                'task_type_multipliers': {k: float(v) for k, v in self.task_type_multipliers.items()},
                'priority_multipliers': {k: float(v) for k, v in self.priority_multipliers.items()},
                'timestamp': time.time()
            }
    
    def import_credits_data(self, data: Dict) -> bool:
        """Импортирует данные кредитной системы"""
        try:
            with self.lock:
                # Импортируем балансы
                self.balances = {node_id: Decimal(str(balance)) for node_id, balance in data.get('balances', {}).items()}
                
                # Импортируем события
                self.events = []
                for event_data in data.get('events', []):
                    event = CreditEvent(
                        event_id=event_data['event_id'],
                        event_type=CreditEventType(event_data['event_type']),
                        timestamp=event_data['timestamp'],
                        from_node=event_data['from_node'],
                        to_node=event_data['to_node'],
                        amount=Decimal(str(event_data['amount'])),
                        task_id=event_data.get('task_id'),
                        description=event_data.get('description')
                    )
                    self.events.append(event)
                
                # Импортируем конфигурацию
                self.resource_rates = {k: Decimal(str(v)) for k, v in data.get('resource_rates', {}).items()}
                self.task_type_multipliers = {k: Decimal(str(v)) for k, v in data.get('task_type_multipliers', {}).items()}
                self.priority_multipliers = {k: Decimal(str(v)) for k, v in data.get('priority_multipliers', {}).items()}
                
                print(f"📥 Импортировано данных для {len(self.balances)} узлов и {len(self.events)} событий")
                return True
                
        except Exception as e:
            print(f"❌ Ошибка импорта данных кредитов: {e}")
            return False
    
    def adjust_resource_rates(self, new_rates: Dict[str, Decimal]) -> bool:
        """Корректирует курсы ресурсов"""
        with self.lock:
            for resource, rate in new_rates.items():
                if resource in self.resource_rates:
                    old_rate = self.resource_rates[resource]
                    self.resource_rates[resource] = rate
                    print(f"📊 Изменен курс для {resource}: {old_rate} -> {rate}")
            
            return True
    
    def get_network_health(self) -> Dict:
        """Получает показатели здоровья кредитной сети"""
        with self.lock:
            if not self.balances:
                return {'healthy': False, 'reason': 'No nodes in credit system'}
            
            # Проверяем распределение кредитов
            total_credits = sum(self.balances.values())
            if total_credits == 0:
                return {'healthy': False, 'reason': 'No credits in system'}
            
            # Проверяем концентрацию (ни один узел не должен иметь более 50% всех кредитов)
            max_balance = max(self.balances.values())
            concentration_ratio = float(max_balance / total_credits)
            
            # Проверяем активность
            recent_events = [e for e in self.events if time.time() - e.timestamp < 3600]  # Последний час
            recent_activity = len(recent_events)
            
            health_score = 100
            issues = []
            
            if concentration_ratio > 0.5:
                health_score -= 30
                issues.append("High credit concentration")
            
            if recent_activity < 5:
                health_score -= 20
                issues.append("Low recent activity")
            
            if len(self.balances) < 3:
                health_score -= 20
                issues.append("Too few nodes")
            
            # Проверяем среднюю загрузку ресурсов (если есть данные)
            avg_cpu_usage = 0.0
            avg_gpu_usage = 0.0
            nodes_with_usage_data = 0
            
            # Это упрощенная проверка. В реальной системе здесь был бы запрос к узлам
            # или к менеджеру ресурсов для получения актуальных данных.
            # Пока используем заглушку.
            if hasattr(self, '_get_average_usage'):
                avg_cpu_usage, avg_gpu_usage = self._get_average_usage()
                nodes_with_usage_data = len(self.balances)
            
            if avg_cpu_usage > 90 or avg_gpu_usage > 90:
                health_score -= 10
                issues.append(f"High resource usage: CPU={avg_cpu_usage:.1f}%, GPU={avg_gpu_usage:.1f}%")
            
            return {
                'healthy': health_score > 50,
                'health_score': health_score,
                'issues': issues,
                'concentration_ratio': concentration_ratio,
                'recent_activity': recent_activity,
                'total_nodes': len(self.balances),
                'total_credits': float(total_credits),
                'avg_cpu_usage': avg_cpu_usage,
                'avg_gpu_usage': avg_gpu_usage
            }

# Пример использования
if __name__ == "__main__":
    # Создаем менеджер кредитов
    credit_manager = CreditManager()
    
    # Инициализируем узлы
    credit_manager.initialize_node("node1", Decimal('100.0'))
    credit_manager.initialize_node("node2", Decimal('50.0'))
    
    # Проверяем балансы
    print(f"Баланс node1: {credit_manager.get_balance('node1')}")
    print(f"Баланс node2: {credit_manager.get_balance('node2')}")
    
    # Переводим кредиты
    credit_manager.transfer_credits("node1", "node2", Decimal('10.0'), "task_123")
    
    # Проверяем балансы после перевода
    print(f"Баланс node1 после перевода: {credit_manager.get_balance('node1')}")
    print(f"Баланс node2 после перевода: {credit_manager.get_balance('node2')}")
    
    # Рассчитываем стоимость задачи
    resource_usage = {
        'cpu_seconds': 10.0,
        'gpu_seconds': 5.0,
        'ram_gb_hours': 1.0
    }
    
    node_capabilities = {
        'cpu_score': 100,
        'gpu_score': 200,
        'ram_gb': 16
    }
    
    cost = credit_manager.calculate_task_cost('ml_inference', 'high', resource_usage, node_capabilities)
    print(f"Стоимость ML inference задачи: {cost}")
    
    # Обрабатываем выполнение задачи
    success, final_cost = credit_manager.process_task_execution(
        "task_123", "node1", "node2", "ml_inference", "high", resource_usage, node_capabilities
    )
    
    print(f"Задача выполнена: {success}, Стоимость: {final_cost}")