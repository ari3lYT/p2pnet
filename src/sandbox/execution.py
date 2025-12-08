#!/usr/bin/env python3
"""
Sandbox система для безопасного исполнения задач
"""

import asyncio
import json
import time
import os
import tempfile
import shutil
import subprocess
import threading
import signal
import resource
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import psutil
import multiprocessing
from concurrent.futures import TimeoutError

class ExecutionStatus(Enum):
    """Статусы исполнения"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    KILLED = "killed"

class SandboxType(Enum):
    """Типы sandbox"""
    WASM = "wasm"
    CONTAINER = "container"
    PROCESS_ISOLATION = "process_isolation"

@dataclass
class ResourceLimits:
    """Лимиты ресурсов"""
    cpu_time_seconds: int = 30
    memory_bytes: int = 100 * 1024 * 1024  # 100MB
    file_size_bytes: int = 50 * 1024 * 1024  # 50MB
    process_count: int = 10
    network_access: bool = False
    disk_access: bool = False
    temp_dir_size: int = 200 * 1024 * 1024  # 200MB

@dataclass
class ExecutionResult:
    """Результат исполнения"""
    status: ExecutionStatus
    output: str
    error: str
    exit_code: int
    execution_time: float
    peak_memory: int
    cpu_time: float
    killed: bool = False
    timeout: bool = False

class ProcessMonitor:
    """Мониторинг процесса исполнения"""
    
    def __init__(self, pid: int, resource_limits: ResourceLimits):
        self.pid = pid
        self.resource_limits = resource_limits
        self.process = psutil.Process(pid)
        self.start_time = time.time()
        self.peak_memory = 0
        self.cpu_time = 0
        self.killed = False
        
        # Запускаем мониторинг в отдельном потоке
        self.monitor_thread = threading.Thread(target=self._monitor)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def _monitor(self):
        """Мониторит процесс и проверяет лимиты"""
        try:
            while not self.killed:
                try:
                    # Проверяем память
                    memory_info = self.process.memory_info()
                    current_memory = memory_info.rss
                    self.peak_memory = max(self.peak_memory, current_memory)
                    
                    # Проверяем CPU время
                    cpu_times = self.process.cpu_times()
                    self.cpu_time = cpu_times.user + cpu_times.system
                    
                    # Проверяем лимиты
                    if current_memory > self.resource_limits.memory_bytes:
                        print(f"Превышен лимит памяти: {current_memory} > {self.resource_limits.memory_bytes}")
                        self.kill()
                        break
                    
                    if self.cpu_time > self.resource_limits.cpu_time_seconds:
                        print(f"Превышен лимит CPU времени: {self.cpu_time} > {self.resource_limits.cpu_time_seconds}")
                        self.kill()
                        break
                    
                    time.sleep(0.1)
                    
                except psutil.NoSuchProcess:
                    break
                    
        except Exception as e:
            print(f"Ошибка мониторинга процесса {self.pid}: {e}")
    
    def get_stats(self) -> Dict:
        """Получает статистику процесса"""
        return {
            'pid': self.pid,
            'peak_memory': self.peak_memory,
            'cpu_time': self.cpu_time,
            'running_time': time.time() - self.start_time,
            'killed': self.killed
        }
    
    def kill(self):
        """Убивает процесс"""
        try:
            self.process.kill()
            self.killed = True
            print(f"Процесс {self.pid} убит")
        except psutil.NoSuchProcess:
            pass

class WASMSandbox:
    """Sandbox на основе WebAssembly"""
    
    def __init__(self, resource_limits: ResourceLimits):
        self.resource_limits = resource_limits
        self.temp_dir = None
        self.wasm_runtime = None
    
    def setup_environment(self) -> str:
        """Настраивает окружение для WASM"""
        # Создаем временную директорию
        self.temp_dir = tempfile.mkdtemp(prefix="wasm_sandbox_")
        
        # Копируем стандартные библиотеки
        lib_dir = os.path.join(self.temp_dir, "lib")
        os.makedirs(lib_dir, exist_ok=True)
        
        # Создаем стандартные функции WASM
        stdlib = """
        module stdlib {
            // Базовые математические функции
            func add (param i32 i32) (result i32)
            func sub (param i32 i32) (result i32)
            func mul (param i32 i32) (result i32)
            func div (param i32 i32) (result i32)
            
            // Функции работы с массивами
            func array_create (param i32) (result i32)
            func array_get (param i32 i32) (result i32)
            func array_set (param i32 i32 i32)
            
            // Функции вывода (только в буфер)
            func print_i32 (param i32)
            func print_f32 (param f32)
        }
        """
        
        with open(os.path.join(lib_dir, "stdlib.wasm"), "w") as f:
            f.write(stdlib)
        
        return self.temp_dir
    
    def compile_to_wasm(self, code: str) -> str:
        """Компилирует код в WASM (заглушка)"""
        # В реальной реализации здесь будет компилятор в WASM
        # Пока возвращаем заглушку
        wasm_code = """
        (module
            (func $add (param $a i32) (param $b i32) (result i32)
                local.get $a
                local.get $b
                i32.add)
            (export "add" (func $add))
        )
        """
        
        wasm_file = os.path.join(self.temp_dir, "user_code.wasm")
        with open(wasm_file, "w") as f:
            f.write(wasm_code)
        
        return wasm_file
    
    def execute(self, wasm_file: str, input_data: Dict) -> ExecutionResult:
        """Выполняет WASM код"""
        start_time = time.time()
        
        try:
            # Запускаем WASM runtime (заглушка)
            # В реальной реализации здесь был бы запуск wasm-движка
            result = {
                'status': ExecutionStatus.COMPLETED,
                'output': json.dumps(input_data),
                'error': '',
                'exit_code': 0,
                'execution_time': time.time() - start_time,
                'peak_memory': 1024 * 1024,  # 1MB
                'cpu_time': 0.1,
                'killed': False,
                'timeout': False
            }
            
            return ExecutionResult(**result)
            
        except Exception as e:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                output='',
                error=str(e),
                exit_code=1,
                execution_time=time.time() - start_time,
                peak_memory=0,
                cpu_time=0,
                killed=False,
                timeout=False
            )
    
    def cleanup(self):
        """Очищает временную директорию"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

class ContainerSandbox:
    """Sandbox на основе контейнеров"""
    
    def __init__(self, resource_limits: ResourceLimits):
        self.resource_limits = resource_limits
        self.container_id = None
        self.temp_dir = None
    
    def create_container(self) -> str:
        """Создает изолированный контейнер"""
        self.temp_dir = tempfile.mkdtemp(prefix="container_sandbox_")
        
        # Создаем Dockerfile для контейнера
        dockerfile_content = """
        FROM python:3.9-slim
        
        # Устанавливаем ограничения ресурсов
        RUN ulimit -v {memory} && ulimit -t {cpu_time}
        
        # Запрещаем сетевой доступ
        ENV NETWORK_DISABLED=true
        
        # Монтируем временную директорию
        VOLUME /tmp/sandbox
        
        # Запускаем с ограниченными правами
        USER nobody
        """
        
        dockerfile_content = dockerfile_content.format(
            memory=self.resource_limits.memory_bytes,
            cpu_time=self.resource_limits.cpu_time_seconds
        )
        
        dockerfile_path = os.path.join(self.temp_dir, "Dockerfile")
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_content)
        
        # Собираем контейнер
        try:
            build_cmd = f"docker build -t sandbox-container {self.temp_dir}"
            subprocess.run(build_cmd, shell=True, check=True, capture_output=True)
            
            # Запускаем контейнер
            run_cmd = f"""
            docker run --rm \
                --memory={self.resource_limits.memory_bytes} \
                --cpus={self.resource_limits.cpu_time_seconds} \
                --network=none \
                -v {self.temp_dir}/tmp:/tmp/sandbox \
                sandbox-container \
                sleep infinity
            """
            
            result = subprocess.run(run_cmd, shell=True, capture_output=True)
            if result.returncode == 0:
                # Извлекаем ID контейнера
                container_id = result.stdout.decode().strip().split('\n')[-1]
                self.container_id = container_id
                return container_id
            else:
                raise Exception(f"Failed to start container: {result.stderr.decode()}")
                
        except subprocess.CalledProcessError as e:
            raise Exception(f"Container creation failed: {e}")
    
    def execute_in_container(self, code: str, input_data: Dict) -> ExecutionResult:
        """Выполняет код в контейнере"""
        start_time = time.time()
        
        try:
            if not self.container_id:
                self.create_container()
            
            # Копируем код в контейнер
            code_file = os.path.join(self.temp_dir, "code.py")
            with open(code_file, "w") as f:
                f.write(code)
            
            copy_cmd = f"docker cp {code_file} {self.container_id}:/tmp/sandbox/code.py"
            subprocess.run(copy_cmd, shell=True, check=True)
            
            # Выполняем код в контейнере
            exec_cmd = f"""
            docker exec {self.container_id} python3 -c "
            import json
            import sys
            import os
            import resource
            
            # Устанавливаем ограничения
            resource.setrlimit(resource.RLIMIT_AS, ({self.resource_limits.memory_bytes}, {self.resource_limits.memory_bytes}))
            resource.setrlimit(resource.RLIMIT_CPU, ({self.resource_limits.cpu_time_seconds}, {self.resource_limits.cpu_time_seconds}))
            
            # Выполняем код
            try:
                exec(open('/tmp/sandbox/code.py').read())
                print('OK')
            except Exception as e:
                print(f'ERROR: {{e}}', file=sys.stderr)
                sys.exit(1)
            "
            """
            
            result = subprocess.run(exec_cmd, shell=True, capture_output=True, timeout=self.resource_limits.cpu_time_seconds + 10)
            
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                return ExecutionResult(
                    status=ExecutionStatus.COMPLETED,
                    output=result.stdout.decode(),
                    error='',
                    exit_code=0,
                    execution_time=execution_time,
                    peak_memory=self.resource_limits.memory_bytes,
                    cpu_time=min(execution_time, self.resource_limits.cpu_time_seconds),
                    killed=False,
                    timeout=False
                )
            else:
                return ExecutionResult(
                    status=ExecutionStatus.FAILED,
                    output='',
                    error=result.stderr.decode(),
                    exit_code=result.returncode,
                    execution_time=execution_time,
                    peak_memory=self.resource_limits.memory_bytes,
                    cpu_time=min(execution_time, self.resource_limits.cpu_time_seconds),
                    killed=False,
                    timeout=False
                )
                
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                status=ExecutionStatus.TIMEOUT,
                output='',
                error='Execution timeout',
                exit_code=124,
                execution_time=time.time() - start_time,
                peak_memory=self.resource_limits.memory_bytes,
                cpu_time=self.resource_limits.cpu_time_seconds,
                killed=False,
                timeout=True
            )
        except Exception as e:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                output='',
                error=str(e),
                exit_code=1,
                execution_time=time.time() - start_time,
                peak_memory=0,
                cpu_time=0,
                killed=False,
                timeout=False
            )
    
    def cleanup(self):
        """Очищает контейнер и временные файлы"""
        if self.container_id:
            try:
                stop_cmd = f"docker stop {self.container_id}"
                subprocess.run(stop_cmd, shell=True, capture_output=True)
            except:
                pass
        
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

class ProcessIsolationSandbox:
    """Sandbox на основе изоляции процессов"""
    
    def __init__(self, resource_limits: ResourceLimits):
        self.resource_limits = resource_limits
        self.temp_dir = None
    
    def setup_environment(self) -> str:
        """Настраивает окружение"""
        self.temp_dir = tempfile.mkdtemp(prefix="process_sandbox_")
        
        # Создаем временные файлы
        with open(os.path.join(self.temp_dir, "input.json"), "w") as f:
            json.dump({"message": "Hello from sandbox"}, f)
        
        return self.temp_dir
    
    def execute(self, code: str, input_data: Dict) -> ExecutionResult:
        """Выполняет код с изоляцией процесса"""
        start_time = time.time()
        
        try:
            # Записываем код во временный файл
            code_file = os.path.join(self.temp_dir, "user_code.py")
            with open(code_file, "w") as f:
                f.write(code)
            
            # Устанавливаем ограничения через resource module
            import resource
            
            # Ограничиваем память
            resource.setrlimit(resource.RLIMIT_AS, 
                              (self.resource_limits.memory_bytes, self.resource_limits.memory_bytes))
            
            # Ограничиваем CPU время
            resource.setrlimit(resource.RLIMIT_CPU, 
                              (self.resource_limits.cpu_time_seconds, self.resource_limits.cpu_time_seconds))
            
            # Ограничиваем количество файлов
            resource.setrlimit(resource.RLIMIT_NOFILE, 
                              (self.resource_limits.process_count, self.resource_limits.process_count))
            
            # Запускаем код в отдельном процессе
            result = subprocess.run(
                [sys.executable, code_file],
                cwd=self.temp_dir,
                capture_output=True,
                text=True,
                timeout=self.resource_limits.cpu_time_seconds + 5
            )
            
            execution_time = time.time() - start_time
            
            return ExecutionResult(
                status=ExecutionStatus.COMPLETED if result.returncode == 0 else ExecutionStatus.FAILED,
                output=result.stdout,
                error=result.stderr,
                exit_code=result.returncode,
                execution_time=execution_time,
                peak_memory=self.resource_limits.memory_bytes,
                cpu_time=min(execution_time, self.resource_limits.cpu_time_seconds),
                killed=False,
                timeout=False
            )
            
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                status=ExecutionStatus.TIMEOUT,
                output='',
                error='Execution timeout',
                exit_code=124,
                execution_time=time.time() - start_time,
                peak_memory=self.resource_limits.memory_bytes,
                cpu_time=self.resource_limits.cpu_time_seconds,
                killed=False,
                timeout=True
            )
        except Exception as e:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                output='',
                error=str(e),
                exit_code=1,
                execution_time=time.time() - start_time,
                peak_memory=0,
                cpu_time=0,
                killed=False,
                timeout=False
            )
    
    def cleanup(self):
        """Очищает временные файлы"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

class SandboxExecutor:
    """Основной класс для исполнения задач в sandbox"""
    
    def __init__(self, sandbox_type: SandboxType = SandboxType.PROCESS_ISOLATION):
        self.sandbox_type = sandbox_type
        self.sandbox = None
        self.process_monitor = None
        
        # Определяем тип sandbox
        if sandbox_type == SandboxType.WASM:
            self.sandbox = WASMSandbox(self.get_default_limits())
        elif sandbox_type == SandboxType.CONTAINER:
            self.sandbox = ContainerSandbox(self.get_default_limits())
        elif sandbox_type == SandboxType.PROCESS_ISOLATION:
            self.sandbox = ProcessIsolationSandbox(self.get_default_limits())
    
    def get_default_limits(self) -> ResourceLimits:
        """Получает лимиты по умолчанию"""
        return ResourceLimits(
            cpu_time_seconds=30,
            memory_bytes=100 * 1024 * 1024,  # 100MB
            file_size_bytes=50 * 1024 * 1024,  # 50MB
            process_count=10,
            network_access=False,
            disk_access=False,
            temp_dir_size=200 * 1024 * 1024  # 200MB
        )
    
    def set_resource_limits(self, limits: ResourceLimits):
        """Устанавливает лимиты ресурсов"""
        self.sandbox.resource_limits = limits
    
    def execute_task(self, task_type: str, code: str, input_data: Dict) -> ExecutionResult:
        """Выполняет задачу в sandbox"""
        print(f"🔒 Запуск {task_type} задачи в sandbox...")
        
        # Настраиваем окружение
        if hasattr(self.sandbox, 'setup_environment'):
            self.sandbox.setup_environment()
        
        # Компилируем код (если нужно)
        wasm_file = None
        if self.sandbox_type == SandboxType.WASM:
            wasm_file = self.sandbox.compile_to_wasm(code)
        
        # Запускаем мониторинг процесса
        if self.sandbox_type == SandboxType.PROCESS_ISOLATION:
            # Для изоляции процессов создаем дочерний процесс
            pid = os.getpid()
            self.process_monitor = ProcessMonitor(pid, self.sandbox.resource_limits)
        
        # Выполняем код
        if wasm_file:
            result = self.sandbox.execute(wasm_file, input_data)
        else:
            result = self.sandbox.execute(code, input_data)
        
        # Получаем статистику
        if self.process_monitor:
            monitor_stats = self.process_monitor.get_stats()
            result.peak_memory = monitor_stats['peak_memory']
            result.cpu_time = monitor_stats['cpu_time']
        
        # Очищаем
        self.sandbox.cleanup()
        
        print(f"✅ Задача выполнена: {result.status.value}")
        return result
    
    def validate_code(self, task_type: str, code: str) -> Tuple[bool, List[str]]:
        """Валидирует код на безопасность"""
        errors = []
        
        # Проверяем запрещенные операции
        forbidden_patterns = [
            'import os',
            'import subprocess',
            'import socket',
            'import sys',
            'import __import__',
            'eval(',
            'exec(',
            'compile(',
            'open(',
            'file(',
            'input(',
            'raw_input(',
            'exit(',
            'quit(',
            'globals()',
            'locals()',
            'vars()',
            'dir()',
            'help()',
            'breakpoint()',
            '__import__',
            'reload(',
            'execfile(',
            'input(',
            'file(',
            'open(',
            'exec(',
            'eval(',
            'compile(',
        ]
        
        for pattern in forbidden_patterns:
            if pattern in code:
                errors.append(f"Forbidden pattern: {pattern}")
        
        # Проверяем специфичные для типа задачи ограничения
        if task_type == 'ml_inference':
            # Разрешаем только безопасные ML операции
            allowed_ml_patterns = [
                'torch.',
                'tensorflow.',
                'numpy.',
                'inference',
                'predict',
                'forward'
            ]
            
            has_ml_code = any(pattern in code for pattern in allowed_ml_patterns)
            if not has_ml_code:
                errors.append("ML inference code must contain ML framework operations")
        
        elif task_type == 'matrix_ops':
            # Разрешаем только математические операции
            allowed_math_patterns = [
                'numpy.',
                'matrix',
                'multiply',
                'add',
                'subtract',
                'dot',
                'transpose'
            ]
            
            has_math_code = any(pattern in code for pattern in allowed_math_patterns)
            if not has_math_code:
                errors.append("Matrix operations code must contain mathematical operations")
        
        return len(errors) == 0, errors

# Пример использования
if __name__ == "__main__":
    # Создаем sandbox executor
    executor = SandboxExecutor(SandboxType.PROCESS_ISOLATION)
    
    # Пример безопасного кода
    safe_code = """
# Безопасный код для вычисления суммы
def calculate_sum(data):
    return sum(data)

# Используем входные данные
input_data = json.loads(open('input.json').read())
result = calculate_sum(input_data.get('numbers', []))
print(result)
"""
    
    # Пример небезопасного кода
    unsafe_code = """
# Небезопасный код
import os
os.system('rm -rf /')
print("This should not be executed")
"""
    
    # Валидируем код
    is_safe, errors = executor.validate_code('range_reduce', safe_code)
    print(f"Безопасный код: {is_safe}, Ошибки: {errors}")
    
    is_safe, errors = executor.validate_code('range_reduce', unsafe_code)
    print(f"Небезопасный код: {is_safe}, Ошибки: {errors}")
    
    # Выполняем безопасный код
    input_data = {"numbers": [1, 2, 3, 4, 5]}
    result = executor.execute_task('range_reduce', safe_code, input_data)
    print(f"Результат: {result}")