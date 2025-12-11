#!/usr/bin/env python3
"""
Система динамического ценообразования для compute-кредитов
"""

import statistics
import time
from collections import defaultdict, deque
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Dict, List, Optional


class PricingFactor(Enum):
    """Факторы влияния на ценообразование"""
    RESOURCE_DEMAND = "resource_demand"
    NETWORK_LOAD = "network_load"
    TASK_URGENCY = "task_urgency"
    NODE_REPUTATION = "node_reputation"
    RESOURCE_SCARCITY = "resource_scarcity"
    MARKET_CONDITIONS = "market_conditions"

class MarketCondition(Enum):
    """Условия рынка"""
    LOW_DEMAND = "low_demand"
    NORMAL = "normal"
    HIGH_DEMAND = "high_demand"
    CRITICAL = "critical"

@dataclass
class PricingConfig:
    """Конфигурация ценообразования"""
    base_cpu_price: float = 0.01
    base_gpu_price: float = 0.05
    base_ram_price: float = 0.02
    base_disk_price: float = 0.005
    
    # Множители
    urgency_multiplier: Dict[str, float] = None
    reputation_multiplier: Dict[str, float] = None
    scarcity_multiplier: float = 1.2
    
    # Пороги
    high_demand_threshold: int = 80
    critical_demand_threshold: int = 95
    
    # Параметры рынка
    market_adjustment_rate: float = 0.1
    price_smoothing: float = 0.3
    
    def __post_init__(self):
        if self.urgency_multiplier is None:
            self.urgency_multiplier = {
                "low": 0.8,
                "normal": 1.0,
                "high": 1.5,
                "critical": 2.0
            }
        
        if self.reputation_multiplier is None:
            self.reputation_multiplier = {
                "terrible": 1.5,
                "poor": 1.2,
                "average": 1.0,
                "good": 0.9,
                "excellent": 0.8
            }

@dataclass
class ResourceMetrics:
    """Метрики ресурсов"""
    cpu_usage: float = 0.0
    gpu_usage: float = 0.0
    ram_usage: float = 0.0
    disk_usage: float = 0.0
    active_tasks: int = 0
    available_nodes: int = 0
    
    def get_demand_level(self) -> str:
        """Определяет уровень спроса"""
        if max(self.cpu_usage, self.gpu_usage) >= self.critical_demand_threshold:
            return "critical"
        elif max(self.cpu_usage, self.gpu_usage) >= self.high_demand_threshold:
            return "high"
        elif max(self.cpu_usage, self.gpu_usage) >= 60:
            return "normal"
        else:
            return "low"

class MarketAnalyzer:
    """Анализатор рыночных условий"""
    
    def __init__(self):
        # История метрик
        self.metrics_history: deque = deque(maxlen=1000)
        self.price_history: deque = deque(maxlen=1000)
        
        # Тренды
        self.cpu_trend = 0.0
        self.gpu_trend = 0.0
        self.ram_trend = 0.0
        
        # Волатильность
        self.cpu_volatility = 0.0
        self.gpu_volatility = 0.0
        
        # Период анализа
        self.analysis_window = 3600  # 1 час
    
    def add_metrics(self, metrics: ResourceMetrics):
        """Добавляет метрики в историю"""
        self.metrics_history.append({
            'timestamp': time.time(),
            'metrics': metrics
        })
    
    def calculate_trends(self) -> Dict[str, float]:
        """Рассчитывает тренды использования ресурсов"""
        if len(self.metrics_history) < 10:
            return {'cpu': 0.0, 'gpu': 0.0, 'ram': 0.0}
        
        recent_metrics = list(self.metrics_history)[-50:]  # Последние 50 записей
        
        # Извлекаем значения
        cpu_values = [m['metrics'].cpu_usage for m in recent_metrics]
        gpu_values = [m['metrics'].gpu_usage for m in recent_metrics]
        ram_values = [m['metrics'].ram_usage for m in recent_metrics]
        
        # Рассчитываем линейные тренды
        def linear_trend(values):
            if len(values) < 2:
                return 0.0
            
            x = list(range(len(values)))
            y = values
            
            # Линейная регрессия
            n = len(values)
            sum_x = sum(x)
            sum_y = sum(y)
            sum_xy = sum(xi * yi for xi, yi in zip(x, y))
            sum_x2 = sum(xi * xi for xi in x)
            
            if n * sum_x2 - sum_x * sum_x == 0:
                return 0.0
            
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
            return slope
        
        self.cpu_trend = linear_trend(cpu_values)
        self.gpu_trend = linear_trend(gpu_values)
        self.ram_trend = linear_trend(ram_values)
        
        # Рассчитываем волатильность
        self.cpu_volatility = statistics.stdev(cpu_values) if len(cpu_values) > 1 else 0.0
        self.gpu_volatility = statistics.stdev(gpu_values) if len(gpu_values) > 1 else 0.0
        
        return {
            'cpu': self.cpu_trend,
            'gpu': self.gpu_trend,
            'ram': self.ram_trend,
            'cpu_volatility': self.cpu_volatility,
            'gpu_volatility': self.gpu_volatility
        }
    
    def predict_demand(self, resource_type: str, time_horizon: int = 3600) -> float:
        """Прогнозирует спрос на ресурс"""
        trends = self.calculate_trends()
        
        current_metrics = self.metrics_history[-1]['metrics'] if self.metrics_history else ResourceMetrics()
        
        if resource_type == 'cpu':
            current_usage = current_metrics.cpu_usage
            trend = trends['cpu']
        elif resource_type == 'gpu':
            current_usage = current_metrics.gpu_usage
            trend = trends['gpu']
        elif resource_type == 'ram':
            current_usage = current_metrics.ram_usage
            trend = trends['ram']
        else:
            # Возвращаем 0.0 для неизвестных типов ресурсов
            return 0.0
        
        # Прогноз: текущее значение + тренд * время горизонта
        predicted_usage = current_usage + trend * (time_horizon / 3600)
        
        # Ограничиваем диапазон
        return max(0, min(100, predicted_usage))
    
    def get_market_condition(self) -> MarketCondition:
        """Определяет текущие рыночные условия"""
        if not self.metrics_history:
            return MarketCondition.NORMAL
        
        latest_metrics = self.metrics_history[-1]['metrics']
        max_usage = max(latest_metrics.cpu_usage, latest_metrics.gpu_usage)
        
        if max_usage >= 95:
            return MarketCondition.CRITICAL
        elif max_usage >= 80:
            return MarketCondition.HIGH_DEMAND
        elif max_usage >= 60:
            return MarketCondition.NORMAL
        else:
            return MarketCondition.LOW_DEMAND

class DynamicPricingEngine:
    """Движок динамического ценообразования"""
    
    def __init__(self, config: PricingConfig):
        self.config = config
        self.market_analyzer = MarketAnalyzer()
        self.current_prices = {
            'cpu': config.base_cpu_price,
            'gpu': config.base_gpu_price,
            'ram': config.base_ram_price,
            'disk': config.base_disk_price
        }
        
        # Кэш цен
        self.price_cache = {}
        self.last_update = {}
        
        # История цен для сглаживания
        self.price_history = defaultdict(lambda: deque(maxlen=100))
    
    def update_market_metrics(self, metrics: ResourceMetrics):
        """Обновляет рыночные метрики"""
        self.market_analyzer.add_metrics(metrics)
        
        # Обновляем цены на основе новых метрик
        self._adjust_prices()
    
    def _adjust_prices(self):
        """Корректирует цены на основе рыночных условий"""
        market_condition = self.market_analyzer.get_market_condition()
        trends = self.market_analyzer.calculate_trends()
        
        # Базовые множители
        condition_multipliers = {
            MarketCondition.LOW_DEMAND: 0.8,
            MarketCondition.NORMAL: 1.0,
            MarketCondition.HIGH_DEMAND: 1.3,
            MarketCondition.CRITICAL: 1.8
        }
        
        base_multiplier = condition_multipliers[market_condition]
        
        # Учитываем тренды
        cpu_trend_factor = 1.0 + max(0, trends['cpu'] * 0.1)
        gpu_trend_factor = 1.0 + max(0, trends['gpu'] * 0.1)
        
        # Учитываем волатильность
        volatility_factor = 1.0 + (trends.get('cpu_volatility', 0) + trends.get('gpu_volatility', 0)) * 0.05
        
        # Рассчитываем новые цены
        new_prices = {}
        
        # CPU цена
        cpu_base = self.config.base_cpu_price * base_multiplier * cpu_trend_factor * volatility_factor
        new_prices['cpu'] = max(0.001, cpu_base)  # Минимальная цена
        
        # GPU цена
        gpu_base = self.config.base_gpu_price * base_multiplier * gpu_trend_factor * volatility_factor
        new_prices['gpu'] = max(0.001, gpu_base)
        
        # RAM цена
        ram_base = self.config.base_ram_price * base_multiplier * volatility_factor
        new_prices['ram'] = max(0.001, ram_base)
        
        # Disk цена
        disk_base = self.config.base_disk_price * base_multiplier * volatility_factor
        new_prices['disk'] = max(0.001, disk_base)
        
        # Применяем сглаживание
        for resource, new_price in new_prices.items():
            old_price = self.current_prices[resource]
            smoothed_price = old_price * (1 - self.config.price_smoothing) + new_price * self.config.price_smoothing
            self.current_prices[resource] = smoothed_price
            self.price_history[resource].append(smoothed_price)
    
    def calculate_task_price(self, task_type: str, priority: str, resource_requirements: Dict,
                           node_reputation: str = "average", node_capabilities: Dict = None) -> Dict[str, float]:
        """Рассчитывает стоимость задачи"""
        
        if node_capabilities is None:
            node_capabilities = {}
        
        # Базовые цены
        base_prices = {
            'range_reduce': {'cpu': 1.0, 'gpu': 0.0, 'ram': 0.5, 'disk': 0.1},
            'map': {'cpu': 1.2, 'gpu': 0.0, 'ram': 0.5, 'disk': 0.1},
            'map_reduce': {'cpu': 1.5, 'gpu': 0.0, 'ram': 1.0, 'disk': 0.2},
            'matrix_ops': {'cpu': 1.3, 'gpu': 0.5, 'ram': 1.0, 'disk': 0.3},
            'ml_inference': {'cpu': 0.5, 'gpu': 2.0, 'ram': 1.5, 'disk': 0.5},
            'ml_train_step': {'cpu': 1.0, 'gpu': 3.0, 'ram': 2.0, 'disk': 1.0}
        }
        
        # Получаем множители для типа задачи
        task_multipliers = base_prices.get(task_type, {'cpu': 1.0, 'gpu': 0.0, 'ram': 0.5, 'disk': 0.1})
        
        # Множитель срочности
        urgency_multiplier = self.config.urgency_multiplier.get(priority, 1.0)
        
        # Множитель репутации узла
        reputation_multiplier = self.config.reputation_multiplier.get(node_reputation, 1.0)
        
        # Множитель дефицита ресурсов
        scarcity_multiplier = self._calculate_scarcity_multiplier(resource_requirements, node_capabilities)
        
        # Рассчитываем стоимость по каждому ресурсу
        resource_costs = {}
        total_cost = 0.0
        
        for resource in ['cpu', 'gpu', 'ram', 'disk']:
            # Базовая цена за единицу ресурса
            unit_price = self.current_prices.get(resource, 0.01)
            
            # Требования задачи
            requirement = resource_requirements.get(resource, 0)
            
            # Стоимость ресурса для этой задачи
            resource_cost = unit_price * requirement * task_multipliers[resource]
            
            # Применяем множители
            final_cost = resource_cost * urgency_multiplier * reputation_multiplier * scarcity_multiplier
            
            resource_costs[resource] = max(0.001, final_cost)
            total_cost += resource_costs[resource]
        
        return {
            'resource_costs': resource_costs,
            'total_cost': total_cost,
            'factors': {
                'urgency': urgency_multiplier,
                'reputation': reputation_multiplier,
                'scarcity': scarcity_multiplier,
                'market_condition': self.market_analyzer.get_market_condition().value
            }
        }
    
    def _calculate_scarcity_multiplier(self, resource_requirements: Dict, node_capabilities: Dict) -> float:
        """Рассчитывает множитель дефицита ресурсов"""
        if not node_capabilities:
            return self.config.scarcity_multiplier
        
        multiplier = 1.0
        
        # Проверяем каждый запрошенный ресурс
        for resource, required in resource_requirements.items():
            if resource in node_capabilities:
                available = node_capabilities.get(resource, 0)
                
                if available > 0:
                    # Чем меньше доступно относительно требований, тем дороже
                    scarcity_ratio = required / available
                    resource_multiplier = 1.0 + min(2.0, scarcity_ratio * 0.5)
                    multiplier *= resource_multiplier
        
        return min(3.0, multiplier)
    
    def get_optimal_node_for_task(self, task_type: str, priority: str, resource_requirements: Dict,
                                 available_nodes: List[Dict]) -> Optional[Dict]:
        """Находит оптимальный узел для задачи"""
        if not available_nodes:
            return None
        
        best_node = None
        best_score = float('inf')
        
        for node in available_nodes:
            node_id = node.get('node_id')
            capabilities = node.get('capabilities', {})
            reputation = node.get('reputation', 'average')
            
            # Рассчитываем стоимость
            pricing = self.calculate_task_price(
                task_type, priority, resource_requirements, reputation, capabilities
            )
            
            # Рассчитываем score (стоимость + штраф за плохую репутацию)
            reputation_penalty = 1.0
            if reputation == 'terrible':
                reputation_penalty = 2.0
            elif reputation == 'poor':
                reputation_penalty = 1.5
            elif reputation == 'good':
                reputation_penalty = 0.9
            elif reputation == 'excellent':
                reputation_penalty = 0.8
            
            score = pricing['total_cost'] * reputation_penalty
            
            # Учитываем загрузку узла
            cpu_load = capabilities.get('cpu_usage', 0) / 100.0
            gpu_load = capabilities.get('gpu_usage', 0) / 100.0 if capabilities.get('gpu_usage', 0) > 0 else 0
            
            load_penalty = 1.0 + (cpu_load + gpu_load) / 2.0
            score *= load_penalty
            
            if score < best_score:
                best_score = score
                best_node = node
        
        return best_node
    
    def predict_future_prices(self, time_horizon: int = 3600) -> Dict[str, float]:
        """Прогнозирует будущие цены"""
        predictions = {}
        
        for resource in ['cpu', 'gpu', 'ram', 'disk']:
            predicted_demand = self.market_analyzer.predict_demand(resource, time_horizon)
            
            # Базовая цена
            base_price = self.current_prices[resource]
            
            # Множитель на основе прогноза спроса
            demand_factor = 1.0 + (predicted_demand / 100.0) * 0.5
            
            predictions[resource] = base_price * demand_factor
        
        return predictions
    
    def get_pricing_analytics(self) -> Dict:
        """Получает аналитику ценообразования"""
        market_condition = self.market_analyzer.get_market_condition()
        trends = self.market_analyzer.calculate_trends()
        
        # Статистика цен
        price_stats = {}
        for resource, prices in self.price_history.items():
            if prices:
                price_stats[resource] = {
                    'current': self.current_prices[resource],
                    'average': statistics.mean(prices),
                    'min': min(prices),
                    'max': max(prices),
                    'volatility': statistics.stdev(prices) if len(prices) > 1 else 0.0
                }
        
        return {
            'market_condition': market_condition.value,
            'trends': trends,
            'current_prices': self.current_prices,
            'price_statistics': price_stats,
            'metrics_count': len(self.market_analyzer.metrics_history),
            'prediction_1h': self.predict_future_prices(3600),
            'prediction_6h': self.predict_future_prices(6 * 3600)
        }
    
    def export_pricing_data(self) -> Dict:
        """Экспортирует данные ценообразования"""
        return {
            'config': asdict(self.config),
            'current_prices': self.current_prices,
            'price_history': {k: list(v) for k, v in self.price_history.items()},
            'analytics': self.get_pricing_analytics(),
            'timestamp': time.time()
        }

# Пример использования
if __name__ == "__main__":
    # Создаем конфигурацию
    config = PricingConfig(
        base_cpu_price=0.01,
        base_gpu_price=0.05,
        base_ram_price=0.02,
        base_disk_price=0.005,
        high_demand_threshold=80,
        critical_demand_threshold=95
    )
    
    # Создаем движок ценообразования
    pricing_engine = DynamicPricingEngine(config)
    
    # Симулируем обновление метрик
    for i in range(10):
        metrics = ResourceMetrics(
            cpu_usage=30 + i * 5,  # Растущая загрузка CPU
            gpu_usage=20 + i * 3,  # Растущая загрузка GPU
            ram_usage=40 + i * 2,
            disk_usage=10,
            active_tasks=5 + i,
            available_nodes=10
        )
        
        pricing_engine.update_market_metrics(metrics)
        
        # Рассчитываем цену для задачи
        resource_requirements = {
            'cpu': 10.0,  # 10 секунд CPU
            'gpu': 5.0,   # 5 секунд GPU
            'ram': 1.0,   # 1 GB RAM
            'disk': 0.1   # 0.1 GB disk
        }
        
        pricing = pricing_engine.calculate_task_price(
            'ml_inference', 'high', resource_requirements, 'good'
        )
        
        print(f"Итерация {i+1}:")
        print(f"  Рыночное условие: {pricing_engine.market_analyzer.get_market_condition().value}")
        print(f"  Стоимость задачи: {pricing['total_cost']:.4f}")
        print(f"  Факторы: {pricing['factors']}")
        print()
    
    # Получаем аналитику
    analytics = pricing_engine.get_pricing_analytics()
    print("📊 Аналитика ценообразования:")
    print(f"  Текущие цены: {analytics['current_prices']}")
    print(f"  Прогноз на 1 час: {analytics['prediction_1h']}")