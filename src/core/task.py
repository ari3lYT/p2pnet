#!/usr/bin/env python3
"""
Описание задач и их декларативного представления
"""

import json
import time
import uuid
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum

class TaskType(Enum):
    """Типы поддерживаемых задач"""
    RANGE_REDUCE = "range_reduce"
    MAP = "map"
    MAP_REDUCE = "map_reduce"
    MATRIX_OPS = "matrix_ops"
    ML_INFERENCE = "ml_inference"
    ML_TRAIN_STEP = "ml_train_step"

class TaskPriority(Enum):
    """Приоритеты задач"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"

@dataclass
class ResourceRequirements:
    """Требования к ресурсам для задачи"""
    cpu_percent: float = 50.0
    ram_gb: float = 1.0
    gpu_percent: float = 0.0
    vram_gb: float = 0.0
    disk_gb: float = 0.1
    timeout_seconds: int = 300

@dataclass
class TaskConfig:
    """Конфигурация задачи"""
    max_price: float = 0.1
    priority: TaskPriority = TaskPriority.NORMAL
    retry_count: int = 3
    validation_required: bool = True

@dataclass
class RangeReduceTask:
    """Задача range_reduce"""
    start: int
    end: int
    operation: str  # "sum", "product", "average", "min", "max"
    chunk_size: int = 1000

@dataclass
class MapTask:
    """Задача map"""
    data: List[Any]
    function: str  # "square", "increment", "transform", "filter"
    params: Dict[str, Any] = None

@dataclass
class MapReduceTask:
    """Задача map_reduce"""
    data: List[Any]
    map_function: str
    reduce_function: str
    params: Dict[str, Any] = None

@dataclass
class MatrixOpsTask:
    """Задача операций с матрицами"""
    operation: str  # "multiply", "add", "transpose", "inverse", "decompose"
    matrix_a: List[List[float]]
    matrix_b: Optional[List[List[float]]] = None
    params: Dict[str, Any] = None

@dataclass
class MLInferenceTask:
    """Задача ML inference"""
    model_path: str
    input_data: List[Any]
    model_type: str  # "pytorch", "tensorflow", "onnx"
    batch_size: int = 1
    params: Dict[str, Any] = None

@dataclass
class MLTrainStepTask:
    """Задача ML training step (data-parallel)"""
    model_path: str
    training_data: List[Any]
    batch_size: int = 32
    learning_rate: float = 0.001
    epochs: int = 1
    model_type: str = "pytorch"
    params: Dict[str, Any] = None

@dataclass
class Task:
    """Основной класс задачи"""
    task_id: str
    task_type: TaskType
    owner_id: str
    created_at: float
    requirements: ResourceRequirements
    config: TaskConfig
    
    # Конкретные данные задачи
    range_reduce: Optional[RangeReduceTask] = None
    map: Optional[MapTask] = None
    map_reduce: Optional[MapReduceTask] = None
    matrix_ops: Optional[MatrixOpsTask] = None
    ml_inference: Optional[MLInferenceTask] = None
    ml_train_step: Optional[MLTrainStepTask] = None
    
    def __post_init__(self):
        if not self.task_id:
            self.task_id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = time.time()
    
    def to_dict(self) -> Dict:
        """Преобразует задачу в словарь"""
        result = asdict(self)
        result['task_type'] = self.task_type.value
        result['requirements'] = asdict(self.requirements)
        result['config'] = asdict(self.config)
        
        # Удаляем None поля
        result = {k: v for k, v in result.items() if v is not None}
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Создает задачу из словаря"""
        # Преобразуем enum значения
        data['task_type'] = TaskType(data['task_type'])
        data['config']['priority'] = TaskPriority(data['config']['priority'])
        data['requirements'] = ResourceRequirements(**data['requirements'])
        data['config'] = TaskConfig(**data['config'])
        
        # Создаем объект задачи
        return cls(**data)
    
    @classmethod
    def create_range_reduce(cls, owner_id: str, start: int, end: int, operation: str, **kwargs) -> 'Task':
        """Создает задачу range_reduce"""
        task = cls(
            task_id="",
            task_type=TaskType.RANGE_REDUCE,
            owner_id=owner_id,
            created_at=0,
            requirements=ResourceRequirements(**kwargs.get('requirements', {})),
            config=TaskConfig(**kwargs.get('config', {}))
        )
        task.range_reduce = RangeReduceTask(start=start, end=end, operation=operation, **kwargs.get('task_params', {}))
        return task
    
    @classmethod
    def create_map(cls, owner_id: str, data: List[Any], function: str, **kwargs) -> 'Task':
        """Создает задачу map"""
        task = cls(
            task_id="",
            task_type=TaskType.MAP,
            owner_id=owner_id,
            created_at=0,
            requirements=ResourceRequirements(**kwargs.get('requirements', {})),
            config=TaskConfig(**kwargs.get('config', {}))
        )
        task.map = MapTask(data=data, function=function, params=kwargs.get('task_params', {}))
        return task
    
    @classmethod
    def create_map_reduce(cls, owner_id: str, data: List[Any], map_function: str, reduce_function: str, **kwargs) -> 'Task':
        """Создает задачу map_reduce"""
        task = cls(
            task_id="",
            task_type=TaskType.MAP_REDUCE,
            owner_id=owner_id,
            created_at=0,
            requirements=ResourceRequirements(**kwargs.get('requirements', {})),
            config=TaskConfig(**kwargs.get('config', {}))
        )
        task.map_reduce = MapReduceTask(
            data=data,
            map_function=map_function,
            reduce_function=reduce_function,
            params=kwargs.get('task_params', {})
        )
        return task
    
    @classmethod
    def create_matrix_ops(cls, owner_id: str, operation: str, matrix_a: List[List[float]], matrix_b: Optional[List[List[float]]] = None, **kwargs) -> 'Task':
        """Создает задачу операций с матрицами"""
        task = cls(
            task_id="",
            task_type=TaskType.MATRIX_OPS,
            owner_id=owner_id,
            created_at=0,
            requirements=ResourceRequirements(**kwargs.get('requirements', {})),
            config=TaskConfig(**kwargs.get('config', {}))
        )
        task.matrix_ops = MatrixOpsTask(
            operation=operation,
            matrix_a=matrix_a,
            matrix_b=matrix_b,
            params=kwargs.get('task_params', {})
        )
        return task
    
    @classmethod
    def create_ml_inference(cls, owner_id: str, model_path: str, input_data: List[Any], model_type: str, **kwargs) -> 'Task':
        """Создает задачу ML inference"""
        task = cls(
            task_id="",
            task_type=TaskType.ML_INFERENCE,
            owner_id=owner_id,
            created_at=0,
            requirements=ResourceRequirements(
                gpu_percent=100.0,
                vram_gb=2.0,
                **kwargs.get('requirements', {})
            ),
            config=TaskConfig(**kwargs.get('config', {}))
        )
        task.ml_inference = MLInferenceTask(
            model_path=model_path,
            input_data=input_data,
            model_type=model_type,
            batch_size=kwargs.get('task_params', {}).get('batch_size', 1),
            params=kwargs.get('task_params', {})
        )
        return task
    
    @classmethod
    def create_ml_train_step(cls, owner_id: str, model_path: str, training_data: List[Any], **kwargs) -> 'Task':
        """Создает задачу ML training step"""
        task = cls(
            task_id="",
            task_type=TaskType.ML_TRAIN_STEP,
            owner_id=owner_id,
            created_at=0,
            requirements=ResourceRequirements(
                gpu_percent=100.0,
                vram_gb=4.0,
                **kwargs.get('requirements', {})
            ),
            config=TaskConfig(**kwargs.get('config', {}))
        )
        task.ml_train_step = MLTrainStepTask(
            model_path=model_path,
            training_data=training_data,
            batch_size=kwargs.get('task_params', {}).get('batch_size', 32),
            learning_rate=kwargs.get('task_params', {}).get('learning_rate', 0.001),
            epochs=kwargs.get('task_params', {}).get('epochs', 1),
            model_type=kwargs.get('task_params', {}).get('model_type', 'pytorch'),
            params=kwargs.get('task_params', {})
        )
        return task
    
    def get_task_data(self) -> Dict:
        """Получает данные конкретной задачи"""
        if self.task_type == TaskType.RANGE_REDUCE and self.range_reduce:
            return asdict(self.range_reduce)
        elif self.task_type == TaskType.MAP and self.map:
            return asdict(self.map)
        elif self.task_type == TaskType.MAP_REDUCE and self.map_reduce:
            return asdict(self.map_reduce)
        elif self.task_type == TaskType.MATRIX_OPS and self.matrix_ops:
            return asdict(self.matrix_ops)
        elif self.task_type == TaskType.ML_INFERENCE and self.ml_inference:
            return asdict(self.ml_inference)
        elif self.task_type == TaskType.ML_TRAIN_STEP and self.ml_train_step:
            return asdict(self.ml_train_step)
        return {}
    
    def validate(self) -> List[str]:
        """Валидирует задачу и возвращает список ошибок"""
        errors = []
        
        # Проверяем обязательные поля
        if not self.owner_id:
            errors.append("owner_id is required")
        
        if not self.task_type:
            errors.append("task_type is required")
        
        # Проверяем требования к ресурсам
        if self.requirements.cpu_percent < 0 or self.requirements.cpu_percent > 100:
            errors.append("cpu_percent must be between 0 and 100")
        
        if self.requirements.ram_gb <= 0:
            errors.append("ram_gb must be positive")
        
        if self.requirements.gpu_percent < 0 or self.requirements.gpu_percent > 100:
            errors.append("gpu_percent must be between 0 and 100")
        
        # Проверяем конкретные типы задач
        if self.task_type == TaskType.RANGE_REDUCE:
            if not self.range_reduce:
                errors.append("range_reduce data is required")
            elif isinstance(self.range_reduce, dict):
                # Если это словарь (после from_dict), проверяем поля
                if self.range_reduce.get('start', 0) >= self.range_reduce.get('end', 0):
                    errors.append("start must be less than end")
            elif self.range_reduce.start >= self.range_reduce.end:
                errors.append("start must be less than end")
        
        elif self.task_type == TaskType.MAP:
            if not self.map:
                errors.append("map data is required")
            elif not self.map.data:
                errors.append("map data cannot be empty")
        
        elif self.task_type == TaskType.MATRIX_OPS:
            if not self.matrix_ops:
                errors.append("matrix_ops data is required")
            elif not self.matrix_ops.matrix_a:
                errors.append("matrix_a cannot be empty")
        
        elif self.task_type == TaskType.ML_INFERENCE:
            if not self.ml_inference:
                errors.append("ml_inference data is required")
            elif not self.ml_inference.model_path:
                errors.append("model_path is required for ML inference")
        
        elif self.task_type == TaskType.ML_TRAIN_STEP:
            if not self.ml_train_step:
                errors.append("ml_train_step data is required")
            elif not self.ml_train_step.model_path:
                errors.append("model_path is required for ML training")
            elif not self.ml_train_step.training_data:
                errors.append("training_data cannot be empty for ML training")
        
        return errors
    
    def estimate_execution_time(self) -> float:
        """Оценивает время выполнения задачи (в секундах)"""
        base_times = {
            TaskType.RANGE_REDUCE: 0.1,
            TaskType.MAP: 0.05,
            TaskType.MAP_REDUCE: 0.2,
            TaskType.MATRIX_OPS: 0.3,
            TaskType.ML_INFERENCE: 1.0,
            TaskType.ML_TRAIN_STEP: 5.0
        }
        
        base_time = base_times.get(self.task_type, 1.0)
        
        # Учитываем размер данных
        data_size = len(self.get_task_data().get('data', []))
        if data_size > 0:
            base_time *= (1 + data_size / 1000)
        
        # Учитываем требования к ресурсам
        if self.requirements.gpu_percent > 0:
            base_time *= 0.5  # GPU ускоряет выполнение
        
        return base_time
    
    def calculate_cost(self, node_capabilities: Dict) -> float:
        """Рассчитывает стоимость выполнения задачи на конкретном узле"""
        base_prices = {
            TaskType.RANGE_REDUCE: 0.01,
            TaskType.MAP: 0.02,
            TaskType.MAP_REDUCE: 0.05,
            TaskType.MATRIX_OPS: 0.03,
            TaskType.ML_INFERENCE: 0.1,
            TaskType.ML_TRAIN_STEP: 0.2
        }
        
        base_price = base_prices.get(self.task_type, 0.01)
        
        # Учитываем приоритет
        priority_multiplier = {
            TaskPriority.LOW: 0.8,
            TaskPriority.NORMAL: 1.0,
            TaskPriority.HIGH: 1.5
        }
        
        multiplier = priority_multiplier.get(self.config.priority, 1.0)
        
        # Учитываем нагрузку на узле
        cpu_load = node_capabilities.get('cpu_score', 100) / 100.0
        gpu_load = node_capabilities.get('gpu_score', 0) / 100.0 if node_capabilities.get('gpu_score', 0) > 0 else 1.0
        
        load_multiplier = 1.0 + (cpu_load + gpu_load) / 2.0
        
        return base_price * multiplier * load_multiplier

class TaskExecutor:
    """Исполнитель задач"""
    
    def __init__(self):
        self.supported_functions = {
            # Range reduce operations
            'sum': self._sum_range,
            'product': self._product_range,
            'average': self._average_range,
            'min': self._min_range,
            'max': self._max_range,
            
            # Map operations
            'square': self._square_map,
            'increment': self._increment_map,
            'transform': self._transform_map,
            'filter': self._filter_map,
            
            # Matrix operations
            'multiply': self._matrix_multiply,
            'add': self._matrix_add,
            'transpose': self._matrix_transpose,
            'inverse': self._matrix_inverse,
            'decompose': self._matrix_decompose,
            
            # ML operations
            'pytorch_inference': self._pytorch_inference,
            'tensorflow_inference': self._tensorflow_inference,
        }
    
    def execute(self, task: Task) -> Dict:
        """Выполняет задачу"""
        start_time = time.time()
        
        try:
            if task.task_type == TaskType.RANGE_REDUCE:
                result = self._execute_range_reduce(task.range_reduce)
            elif task.task_type == TaskType.MAP:
                result = self._execute_map(task.map)
            elif task.task_type == TaskType.MAP_REDUCE:
                result = self._execute_map_reduce(task.map_reduce)
            elif task.task_type == TaskType.MATRIX_OPS:
                result = self._execute_matrix_ops(task.matrix_ops)
            elif task.task_type == TaskType.ML_INFERENCE:
                result = self._execute_ml_inference(task.ml_inference)
            elif task.task_type == TaskType.ML_TRAIN_STEP:
                result = self._execute_ml_train_step(task.ml_train_step)
            else:
                raise ValueError(f"Unsupported task type: {task.task_type}")
            
            execution_time = time.time() - start_time
            
            return {
                'success': True,
                'result': result,
                'execution_time': execution_time,
                'resource_used': {
                    'cpu_percent': task.requirements.cpu_percent,
                    'ram_gb': task.requirements.ram_gb,
                    'gpu_percent': task.requirements.gpu_percent
                }
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                'success': False,
                'error': str(e),
                'execution_time': execution_time,
                'resource_used': {
                    'cpu_percent': task.requirements.cpu_percent,
                    'ram_gb': task.requirements.ram_gb,
                    'gpu_percent': task.requirements.gpu_percent
                }
            }
    
    def _execute_range_reduce(self, task: RangeReduceTask) -> Any:
        """Выполняет range_reduce задачу"""
        numbers = range(task.start, task.end, task.chunk_size)
        
        if task.operation == 'sum':
            return sum(numbers)
        elif task.operation == 'product':
            result = 1
            for num in numbers:
                result *= num
            return result
        elif task.operation == 'average':
            numbers_list = list(numbers)
            return sum(numbers_list) / len(numbers_list) if numbers_list else 0
        elif task.operation == 'min':
            return min(numbers)
        elif task.operation == 'max':
            return max(numbers)
        else:
            raise ValueError(f"Unknown range_reduce operation: {task.operation}")
    
    def _execute_map(self, task: MapTask) -> List[Any]:
        """Выполняет map задачу"""
        if task.function == 'square':
            return [x ** 2 for x in task.data]
        elif task.function == 'increment':
            increment = task.params.get('increment', 1) if task.params else 1
            return [x + increment for x in task.data]
        elif task.function == 'transform':
            transform_func = task.params.get('function') if task.params else lambda x: x
            return [transform_func(x) for x in task.data]
        elif task.function == 'filter':
            filter_func = task.params.get('function') if task.params else lambda x: True
            return [x for x in task.data if filter_func(x)]
        else:
            raise ValueError(f"Unknown map function: {task.function}")
    
    def _execute_map_reduce(self, task: MapReduceTask) -> Any:
        """Выполняет map_reduce задачу"""
        # Сначала применяем map
        mapped_data = self._execute_map(MapTask(
            data=task.data,
            function=task.map_function,
            params=task.params
        ))
        
        # Затем применяем reduce
        if task.reduce_function == 'sum':
            return sum(mapped_data)
        elif task.reduce_function == 'product':
            result = 1
            for item in mapped_data:
                result *= item
            return result
        elif task.reduce_function == 'count':
            return len(mapped_data)
        else:
            raise ValueError(f"Unknown reduce function: {task.reduce_function}")
    
    def _execute_matrix_ops(self, task: MatrixOpsTask) -> List[List[float]]:
        """Выполняет операции с матрицами"""
        if task.operation == 'transpose':
            return [[task.matrix_a[j][i] for j in range(len(task.matrix_a))] for i in range(len(task.matrix_a[0]))]
        elif task.operation == 'add':
            if not task.matrix_b:
                raise ValueError("Matrix B is required for addition")
            return [[task.matrix_a[i][j] + task.matrix_b[i][j] for j in range(len(task.matrix_a[0]))] for i in range(len(task.matrix_a))]
        elif task.operation == 'multiply':
            if not task.matrix_b:
                raise ValueError("Matrix B is required for multiplication")
            result = [[0 for _ in range(len(task.matrix_b[0]))] for _ in range(len(task.matrix_a))]
            for i in range(len(task.matrix_a)):
                for j in range(len(task.matrix_b[0])):
                    for k in range(len(task.matrix_b)):
                        result[i][j] += task.matrix_a[i][k] * task.matrix_b[k][j]
            return result
        else:
            # Для сложных операций (inverse, decompose) нужны внешние библиотеки
            raise NotImplementedError(f"Matrix operation {task.operation} not implemented")
    
    def _execute_ml_inference(self, task: MLInferenceTask) -> Dict:
        """Выполняет ML inference задачу"""
        # Здесь будет реальное выполнение ML модели
        # Пока возвращаем заглушку
        return {
            'predictions': [0.5] * len(task.input_data),
            'model_info': {
                'model_path': task.model_path,
                'model_type': task.model_type,
                'batch_size': task.batch_size
            }
        }
    
    def _execute_ml_train_step(self, task: MLTrainStepTask) -> Dict:
        """Выполняет ML training step задачу"""
        # Здесь будет реальное обучение ML модели
        # Пока возвращаем заглушку
        return {
            'loss': 0.1,
            'accuracy': 0.95,
            'model_updated': True,
            'training_info': {
                'model_path': task.model_path,
                'epochs': task.epochs,
                'batch_size': task.batch_size,
                'learning_rate': task.learning_rate
            }
        }
    
    # Вспомогательные функции для map операций
    def _sum_range(self, data):
        return sum(data)
    
    def _product_range(self, data):
        result = 1
        for item in data:
            result *= item
        return result
    
    def _average_range(self, data):
        return sum(data) / len(data) if data else 0
    
    def _min_range(self, data):
        return min(data)
    
    def _max_range(self, data):
        return max(data)
    
    def _square_map(self, data):
        return [x ** 2 for x in data]
    
    def _increment_map(self, data):
        increment = 1
        return [x + increment for x in data]
    
    def _transform_map(self, data):
        return data  # Реальная трансформация зависит от params
    
    def _filter_map(self, data):
        return data  # Реальная фильтрация зависит от params
    
    def _matrix_multiply(self, a, b):
        return self._execute_matrix_ops(MatrixOpsTask('multiply', a, b))
    
    def _matrix_add(self, a, b):
        return self._execute_matrix_ops(MatrixOpsTask('add', a, b))
    
    def _matrix_transpose(self, matrix):
        return self._execute_matrix_ops(MatrixOpsTask('transpose', matrix))
    
    def _matrix_inverse(self, matrix):
        raise NotImplementedError("Matrix inverse not implemented")
    
    def _matrix_decompose(self, matrix):
        raise NotImplementedError("Matrix decomposition not implemented")
    
    def _pytorch_inference(self, model_path, input_data):
        return self._execute_ml_inference(MLInferenceTask(model_path, input_data, 'pytorch'))
    
    def _tensorflow_inference(self, model_path, input_data):
        return self._execute_ml_inference(MLInferenceTask(model_path, input_data, 'tensorflow'))