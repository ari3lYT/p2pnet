#!/usr/bin/env python3
"""
Система репутации для децентрализованной вычислительной сети
"""

import json
import time
import asyncio
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
import statistics
import hashlib

class ReputationEventType(Enum):
    """Типы событий репутации"""
    TASK_SUCCESS = "task_success"
    TASK_FAILURE = "task_failure"
    CHEAT_DETECTED = "cheat_detected"
    MALICIOUS_BEHAVIOR = "malicious_behavior"
    COOPERATIVE_BEHAVIOR = "cooperative_behavior"
    LONGEVITY_BONUS = "longevity_bonus"
    QUALITY_BONUS = "quality_bonus"

@dataclass
class ReputationEvent:
    """Событие репутации"""
    event_id: str
    event_type: ReputationEventType
    node_id: str
    timestamp: float
    task_id: Optional[str] = None
    description: Optional[str] = None
    severity: float = 1.0  # 0.1 (легкий) до 10.0 (тяжелый)
    
    def to_dict(self) -> Dict:
        result = asdict(self)
        result['event_type'] = self.event_type.value
        result['severity'] = float(self.severity)
        return {k: v for k, v in result.items() if v is not None}

class ReputationScore:
    """Класс для расчета репутационного балла"""
    
    def __init__(self):
        # Весовые коэффициенты
        self.weights = {
            'success_rate': 0.3,
            'task_quality': 0.25,
            'consistency': 0.2,
            'longevity': 0.15,
            'cooperation': 0.1
        }
        
        # Параметры времени
        self.decay_rate = 0.01  # Скорость старения репутации
        self.recent_timeframe = 30 * 24 * 3600  # 30 дней
    
    def calculate_success_rate(self, events: List[ReputationEvent]) -> float:
        """Рассчитывает успешность выполнения задач"""
        recent_events = [e for e in events if time.time() - e.timestamp < self.recent_timeframe]
        
        if not recent_events:
            return 0.5  # Нейтральная оценка
        
        successes = sum(1 for e in recent_events if e.event_type == ReputationEventType.TASK_SUCCESS)
        total = len([e for e in recent_events if e.event_type in [ReputationEventType.TASK_SUCCESS, ReputationEventType.TASK_FAILURE]])
        
        if total == 0:
            return 0.5
        
        return successes / total
    
    def calculate_task_quality(self, events: List[ReputationEvent]) -> float:
        """Рассчитывает качество выполнения задач"""
        quality_events = [e for e in events if e.event_type == ReputationEventType.QUALITY_BONUS]
        
        if not quality_events:
            return 0.5
        
        # Учитываем время и вес
        current_time = time.time()
        total_quality = 0
        total_weight = 0
        
        for event in quality_events:
            age_factor = max(0, 1 - (current_time - event.timestamp) / self.recent_timeframe)
            weight = event.severity * age_factor
            total_quality += weight
            total_weight += weight
        
        return total_quality / total_weight if total_weight > 0 else 0.5
    
    def calculate_consistency(self, events: List[ReputationEvent]) -> float:
        """Рассчитывает последовательность выполнения"""
        task_events = [e for e in events if e.event_type in [ReputationEventType.TASK_SUCCESS, ReputationEventType.TASK_FAILURE]]
        
        if len(task_events) < 5:
            return 0.5
        
        # Рассчитываем стандартное отклонение времени выполнения
        execution_times = []
        for i in range(1, len(task_events)):
            time_diff = task_events[i].timestamp - task_events[i-1].timestamp
            execution_times.append(time_diff)
        
        if not execution_times:
            return 0.5
        
        std_dev = statistics.stdev(execution_times) if len(execution_times) > 1 else 0
        
        # Нормализуем (меньше отклонение = выше оценка)
        max_std = 3600  # 1 час
        consistency = max(0, 1 - (std_dev / max_std))
        
        return consistency
    
    def calculate_longevity(self, events: List[ReputationEvent]) -> float:
        """Рассчитывает долгосрочность участия"""
        if not events:
            return 0.0
        
        first_event = min(events, key=lambda e: e.timestamp)
        age = time.time() - first_event.timestamp
        
        # Логарифмическая шкала для долгосрочности
        max_age = 365 * 24 * 3600  # 1 год
        longevity = min(1.0, age / max_age)
        
        return longevity
    
    def calculate_cooperation(self, events: List[ReputationEvent]) -> float:
        """Рассчитывает уровень сотрудничества"""
        cooperative_events = [e for e in events if e.event_type == ReputationEventType.COOPERATIVE_BEHAVIOR]
        malicious_events = [e for e in events if e.event_type == ReputationEventType.MALICIOUS_BEHAVIOR]
        
        if not cooperative_events and not malicious_events:
            return 0.5
        
        cooperative_score = sum(e.severity for e in cooperative_events)
        malicious_score = sum(e.severity for e in malicious_events)
        
        total_score = cooperative_score + malicious_score
        if total_score == 0:
            return 0.5
        
        return cooperative_score / total_score
    
    def calculate_overall_score(self, events: List[ReputationEvent]) -> float:
        """Рассчитывает общий репутационный балл"""
        if not events:
            return 0.5
        
        # Рассчитываем компоненты
        success_rate = self.calculate_success_rate(events)
        task_quality = self.calculate_task_quality(events)
        consistency = self.calculate_consistency(events)
        longevity = self.calculate_longevity(events)
        cooperation = self.calculate_cooperation(events)
        
        # Применяем веса
        overall_score = (
            success_rate * self.weights['success_rate'] +
            task_quality * self.weights['task_quality'] +
            consistency * self.weights['consistency'] +
            longevity * self.weights['longevity'] +
            cooperation * self.weights['cooperation']
        )
        
        # Применяем decay
        current_time = time.time()
        age_factor = 1.0
        if events:
            newest_event = max(events, key=lambda e: e.timestamp)
            age = current_time - newest_event.timestamp
            age_factor = max(0.1, 1.0 - (age / self.recent_timeframe) * self.decay_rate)
        
        return overall_score * age_factor

class ReputationManager:
    """Менеджер репутационной системы"""
    
    def __init__(self):
        # Хранилище событий
        self.events: Dict[str, List[ReputationEvent]] = defaultdict(list)
        
        # Кэш баллов
        self.score_cache: Dict[str, float] = {}
        self.last_calculation: Dict[str, float] = {}
        
        # Система расчета баллов
        self.score_calculator = ReputationScore()
        
        # Пороги для разных уровней репутации
        self.reputation_thresholds = {
            'excellent': 0.9,
            'good': 0.7,
            'average': 0.5,
            'poor': 0.3,
            'terrible': 0.1
        }
        
        # История для анализа
        self.event_history: deque = deque(maxlen=10000)
        
        # Блокировки для потокобезопасности
        self.lock = asyncio.Lock()
    
    async def add_event(self, event: ReputationEvent) -> bool:
        """Добавляет событие репутации"""
        async with self.lock:
            self.events[event.node_id].append(event)
            self.event_history.append(event)
            
            # Инвалидируем кэш для этого узла
            if event.node_id in self.score_cache:
                del self.score_cache[event.node_id]
            
            print(f"📝 Добавлено событие репутации для {event.node_id}: {event.event_type.value}")
            return True
    
    async def get_reputation_score(self, node_id: str, use_cache: bool = True) -> float:
        """Получает репутационный балл узла"""
        async with self.lock:
            # Проверяем кэш
            if use_cache and node_id in self.score_cache:
                current_time = time.time()
                if current_time - self.last_calculation[node_id] < 300:  # 5 минут
                    return self.score_cache[node_id]
            
            # Рассчитываем балл
            events = self.events.get(node_id, [])
            score = self.score_calculator.calculate_overall_score(events)
            
            # Обновляем кэш
            self.score_cache[node_id] = score
            self.last_calculation[node_id] = time.time()
            
            return score
    
    async def get_reputation_level(self, node_id: str) -> str:
        """Получает уровень репутации узла"""
        score = await self.get_reputation_score(node_id)
        
        if score >= self.reputation_thresholds['excellent']:
            return 'excellent'
        elif score >= self.reputation_thresholds['good']:
            return 'good'
        elif score >= self.reputation_thresholds['average']:
            return 'average'
        elif score >= self.reputation_thresholds['poor']:
            return 'poor'
        else:
            return 'terrible'
    
    async def get_reputation_details(self, node_id: str) -> Dict:
        """Получает подробную информацию о репутации"""
        events = self.events.get(node_id, [])
        
        if not events:
            return {
                'node_id': node_id,
                'score': 0.5,
                'level': 'unknown',
                'total_events': 0,
                'components': {},
                'recent_activity': []
            }
        
        # Рассчитываем компоненты
        score = await self.get_reputation_score(node_id)
        level = await self.get_reputation_level(node_id)
        
        components = {
            'success_rate': self.score_calculator.calculate_success_rate(events),
            'task_quality': self.score_calculator.calculate_task_quality(events),
            'consistency': self.score_calculator.calculate_consistency(events),
            'longevity': self.score_calculator.calculate_longevity(events),
            'cooperation': self.score_calculator.calculate_cooperation(events)
        }
        
        # Последние события
        recent_events = sorted(events, key=lambda e: e.timestamp, reverse=True)[:10]
        recent_activity = [
            {
                'type': e.event_type.value,
                'timestamp': e.timestamp,
                'description': e.description,
                'severity': e.severity
            }
            for e in recent_events
        ]
        
        return {
            'node_id': node_id,
            'score': score,
            'level': level,
            'total_events': len(events),
            'components': components,
            'recent_activity': recent_activity
        }
    
    async def process_task_execution(self, task_id: str, node_id: str, 
                                   success: bool, execution_time: float,
                                   resource_used: Dict, validation_passed: bool = True) -> bool:
        """Обрабатывает выполнение задачи и обновляет репутацию"""
        
        if success and validation_passed:
            # Успешное выполнение
            event = ReputationEvent(
                event_id=str(int(time.time() * 1000000)),
                event_type=ReputationEventType.TASK_SUCCESS,
                node_id=node_id,
                task_id=task_id,
                description=f"Task {task_id} completed successfully in {execution_time:.2f}s",
                severity=1.0
            )
            
            # Бонус за качество (быстрое выполнение)
            if execution_time < 5.0:  # Меньше 5 секунд
                quality_event = ReputationEvent(
                    event_id=str(int(time.time() * 1000000 + 1)),
                    event_type=ReputationEventType.QUALITY_BONUS,
                    node_id=node_id,
                    task_id=task_id,
                    description=f"High quality execution of task {task_id}",
                    severity=1.5
                )
                await self.add_event(quality_event)
            
        else:
            # Неудачное выполнение
            event = ReputationEvent(
                event_id=str(int(time.time() * 1000000)),
                event_type=ReputationEventType.TASK_FAILURE,
                node_id=node_id,
                task_id=task_id,
                description=f"Task {task_id} failed" + (", validation failed" if not validation_passed else ""),
                severity=2.0
            )
        
        await self.add_event(event)
        return True
    
    async def detect_cheating(self, task_id: str, node_id: str, evidence: str) -> bool:
        """Обнаружение мошенничества"""
        event = ReputationEvent(
            event_id=str(int(time.time() * 1000000)),
            event_type=ReputationEventType.CHEAT_DETECTED,
            node_id=node_id,
            task_id=task_id,
            description=f"Cheat detected: {evidence}",
            severity=5.0
        )
        
        await self.add_event(event)
        print(f"🚨 Обнаружено мошенничество от узла {node_id}: {evidence}")
        return True
    
    async def reward_cooperation(self, node_id: str, reason: str, severity: float = 1.0) -> bool:
        """Награждает сотрудничество"""
        event = ReputationEvent(
            event_id=str(int(time.time() * 1000000)),
            event_type=ReputationEventType.COOPERATIVE_BEHAVIOR,
            node_id=node_id,
            description=f"Cooperative behavior: {reason}",
            severity=severity
        )
        
        await self.add_event(event)
        return True
    
    async def penalize_malicious(self, node_id: str, reason: str, severity: float = 2.0) -> bool:
        """Штрафует вредоносное поведение"""
        event = ReputationEvent(
            event_id=str(int(time.time() * 1000000)),
            event_type=ReputationEventType.MALICIOUS_BEHAVIOR,
            node_id=node_id,
            description=f"Malicious behavior: {reason}",
            severity=severity
        )
        
        await self.add_event(event)
        print(f"⚠️ Вредоносное поведение от узла {node_id}: {reason}")
        return True
    
    async def get_top_nodes(self, limit: int = 10, min_events: int = 5) -> List[Dict]:
        """Получает топ узлов по репутации"""
        candidates = []
        
        for node_id, events in self.events.items():
            if len(events) >= min_events:
                score = await self.get_reputation_score(node_id)
                candidates.append((node_id, score))
        
        # Сортируем по баллу
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        # Форматируем результат
        result = []
        for node_id, score in candidates[:limit]:
            level = await self.get_reputation_level(node_id)
            result.append({
                'node_id': node_id,
                'score': score,
                'level': level,
                'events_count': len(self.events[node_id])
            })
        
        return result
    
    async def get_network_reputation_stats(self) -> Dict:
        """Получает статистику репутации сети"""
        if not self.events:
            return {'total_nodes': 0, 'average_score': 0.5}
        
        scores = []
        level_counts = defaultdict(int)
        
        for node_id in self.events:
            score = await self.get_reputation_score(node_id)
            level = await self.get_reputation_level(node_id)
            
            scores.append(score)
            level_counts[level] += 1
        
        return {
            'total_nodes': len(self.events),
            'average_score': statistics.mean(scores) if scores else 0.5,
            'median_score': statistics.median(scores) if scores else 0.5,
            'level_distribution': dict(level_counts),
            'score_std': statistics.stdev(scores) if len(scores) > 1 else 0.0
        }
    
    async def cleanup_old_events(self, max_age_days: int = 90) -> int:
        """Удаляет старые события"""
        cutoff_time = time.time() - (max_age_days * 24 * 3600)
        cleaned_count = 0
        
        async with self.lock:
            for node_id, events in list(self.events.items()):
                # Фильтруем старые события
                new_events = [e for e in events if e.timestamp > cutoff_time]
                
                if len(new_events) < len(events):
                    cleaned_count += len(events) - len(new_events)
                    self.events[node_id] = new_events
                    
                    # Инвалидируем кэш
                    if node_id in self.score_cache:
                        del self.score_cache[node_id]
            
            print(f"🧹 Очищено {cleaned_count} старых событий репутации")
            return cleaned_count
    
    async def export_reputation_data(self) -> Dict:
        """Экспортирует данные репутации"""
        async with self.lock:
            return {
                'events': {
                    node_id: [event.to_dict() for event in events]
                    for node_id, events in self.events.items()
                },
                'thresholds': {k: float(v) for k, v in self.reputation_thresholds.items()},
                'weights': {k: float(v) for k, v in self.score_calculator.weights.items()},
                'timestamp': time.time()
            }
    
    async def import_reputation_data(self, data: Dict) -> bool:
        """Импортирует данные репутации"""
        try:
            async with self.lock:
                # Импортируем события
                self.events.clear()
                for node_id, event_list in data.get('events', {}).items():
                    self.events[node_id] = []
                    for event_data in event_list:
                        event = ReputationEvent(
                            event_id=event_data['event_id'],
                            event_type=ReputationEventType(event_data['event_type']),
                            node_id=event_data['node_id'],
                            timestamp=event_data['timestamp'],
                            task_id=event_data.get('task_id'),
                            description=event_data.get('description'),
                            severity=event_data['severity']
                        )
                        self.events[node_id].append(event)
                
                # Импортируем настройки
                self.reputation_thresholds = data.get('thresholds', self.reputation_thresholds)
                self.score_calculator.weights = data.get('weights', self.score_calculator.weights)
                
                print(f"📥 Импортировано данных для {len(self.events)} узлов")
                return True
                
        except Exception as e:
            print(f"❌ Ошибка импорта данных репутации: {e}")
            return False
    
    async def calculate_trust_score(self, node_id: str, context: str = "general") -> float:
        """Рассчитывает доверительный балл в конкретном контексте"""
        base_score = await self.get_reputation_score(node_id)
        
        # Контекстные множители
        context_multipliers = {
            "general": 1.0,
            "compute_intensive": 0.9,
            "ml_training": 0.8,
            "sensitive_data": 0.7,
            "coordinator": 1.2
        }
        
        multiplier = context_multipliers.get(context, 1.0)
        
        # Учитываем время последней активности
        events = self.events.get(node_id, [])
        if events:
            last_activity = max(e.timestamp for e in events)
            age = time.time() - last_activity
            activity_factor = max(0.1, 1.0 - (age / (7 * 24 * 3600)))  # 7 дней
            
            return base_score * multiplier * activity_factor
        
        return base_score * multiplier

# Пример использования
if __name__ == "__main__":
    async def main():
        # Создаем менеджер репутации
        rep_manager = ReputationManager()
        
        # Добавляем события для тестового узла
        node_id = "test_node_123"
        
        # Успешные задачи
        for i in range(10):
            event = ReputationEvent(
                event_id=f"success_{i}",
                event_type=ReputationEventType.TASK_SUCCESS,
                node_id=node_id,
                timestamp=time.time() - i * 3600,  # Раз в час
                task_id=f"task_{i}",
                description=f"Successfully completed task {i}",
                severity=1.0
            )
            await rep_manager.add_event(event)
        
        # Неудачная задача
        failed_event = ReputationEvent(
            event_id="failed_1",
            event_type=ReputationEventType.TASK_FAILURE,
            node_id=node_id,
            timestamp=time.time() - 11 * 3600,
            task_id="task_11",
            description="Task failed due to timeout",
            severity=2.0
        )
        await rep_manager.add_event(failed_event)
        
        # Получаем репутацию
        score = await rep_manager.get_reputation_score(node_id)
        print(f"Репутационный балл узла {node_id}: {score:.3f}")
        
        level = await rep_manager.get_reputation_level(node_id)
        print(f"Уровень репутации: {level}")
        
        # Подробная информация
        details = await rep_manager.get_reputation_details(node_id)
        print(f"Компоненты репутации: {details['components']}")
        
        # Статистика сети
        stats = await rep_manager.get_network_reputation_stats()
        print(f"Статистика сети: {stats}")
    
    # Запускаем тест
    asyncio.run(main())