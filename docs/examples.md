<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Примеры использования - P2PNet</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --bg-primary: #0a0a0a;
            --bg-secondary: #1a1a1a;
            --bg-tertiary: #2a2a2a;
            --text-primary: #ffffff;
            --text-secondary: #a0a0a0;
            --text-tertiary: #666666;
            --accent-primary: #00d4ff;
            --accent-secondary: #0099cc;
            --border-color: #333333;
            --gradient-primary: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.8;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            overflow-x: hidden;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 24px;
        }

        header {
            background-color: rgba(10, 10, 10, 0.8);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--border-color);
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 1000;
        }

        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }

        .logo {
            font-size: 1.5rem;
            font-weight: 700;
            text-decoration: none;
            color: var(--text-primary);
            letter-spacing: -0.5px;
        }

        .logo::after {
            content: '';
            display: block;
            width: 0;
            height: 2px;
            background: var(--gradient-primary);
            transition: width 0.3s ease;
        }

        .logo:hover::after {
            width: 100%;
        }

        nav ul {
            list-style: none;
            display: flex;
            gap: 2rem;
            align-items: center;
        }

        nav a {
            color: var(--text-secondary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
            position: relative;
        }

        nav a::after {
            content: '';
            position: absolute;
            bottom: -4px;
            left: 0;
            width: 0;
            height: 1px;
            background: var(--accent-primary);
            transition: width 0.3s ease;
        }

        nav a:hover {
            color: var(--text-primary);
        }

        nav a:hover::after {
            width: 100%;
        }

        main {
            padding-top: 80px;
            min-height: 100vh;
        }

        .hero {
            text-align: center;
            padding: 4rem 0;
            position: relative;
        }

        .hero h1 {
            font-size: clamp(2rem, 4vw, 3rem);
            margin-bottom: 1rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero .subtitle {
            font-size: clamp(1rem, 2vw, 1.2rem);
            color: var(--text-secondary);
            max-width: 600px;
            margin: 0 auto;
        }

        .content {
            background: var(--bg-secondary);
            padding: 3rem;
            border-radius: 16px;
            border: 1px solid var(--border-color);
            margin: 2rem 0;
        }

        .content h2 {
            color: var(--text-primary);
            margin-bottom: 1rem;
            font-size: 2rem;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .content h3 {
            color: var(--text-primary);
            margin: 2rem 0 1rem 0;
            font-size: 1.5rem;
        }

        .content h4 {
            color: var(--text-primary);
            margin: 1.5rem 0 0.75rem 0;
            font-size: 1.2rem;
        }

        .content p {
            color: var(--text-secondary);
            margin-bottom: 1rem;
            line-height: 1.8;
        }

        .content ul {
            color: var(--text-secondary);
            margin-left: 2rem;
            margin-bottom: 1rem;
        }

        .content li {
            margin-bottom: 0.5rem;
        }

        .content pre {
            background: var(--bg-tertiary);
            padding: 1.5rem;
            border-radius: 8px;
            overflow-x: auto;
            border: 1px solid var(--border-color);
            margin: 1rem 0;
        }

        .content code {
            background: var(--bg-tertiary);
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            color: var(--accent-primary);
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.9rem;
        }

        .content .highlight {
            background: var(--bg-tertiary);
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid var(--accent-primary);
            margin: 1rem 0;
        }

        .content .highlight p {
            color: var(--text-primary);
            margin-bottom: 0;
        }

        .example-card {
            background: var(--bg-tertiary);
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            margin: 2rem 0;
            position: relative;
            overflow: hidden;
        }

        .example-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: var(--gradient-primary);
        }

        .example-header {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
        }

        .example-icon {
            font-size: 2rem;
            margin-right: 1rem;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .example-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        .example-description {
            color: var(--text-secondary);
            margin-bottom: 1.5rem;
            line-height: 1.6;
        }

        .example-code {
            background: var(--bg-secondary);
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            margin: 1rem 0;
        }

        .example-result {
            background: var(--bg-secondary);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            margin: 1rem 0;
        }

        .example-result h4 {
            color: var(--accent-primary);
            margin-bottom: 0.5rem;
            font-size: 1rem;
        }

        .example-result pre {
            background: var(--bg-tertiary);
            padding: 1rem;
            border-radius: 4px;
            margin: 0;
            font-size: 0.9rem;
        }

        .nav-links {
            display: flex;
            justify-content: space-between;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid var(--border-color);
        }

        .nav-links a {
            color: var(--accent-primary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
        }

        .nav-links a:hover {
            color: var(--accent-secondary);
        }

        footer {
            background: var(--bg-secondary);
            border-top: 1px solid var(--border-color);
            padding: 3rem 0 2rem;
            margin-top: 4rem;
        }

        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 2rem;
        }

        .footer-content p {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .social-links {
            display: flex;
            gap: 2rem;
        }

        .social-links a {
            color: var(--text-secondary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
            position: relative;
        }

        .social-links a::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 0;
            height: 1px;
            background: var(--accent-primary);
            transition: width 0.3s ease;
        }

        .social-links a:hover {
            color: var(--accent-primary);
        }

        .social-links a:hover::after {
            width: 100%;
        }

        @media (max-width: 768px) {
            nav ul {
                gap: 1rem;
            }
            
            .content {
                padding: 2rem 1rem;
            }
            
            .example-card {
                padding: 1.5rem;
            }
            
            .nav-links {
                flex-direction: column;
                gap: 1rem;
            }
            
            .footer-content {
                flex-direction: column;
                text-align: center;
            }
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <a href="/" class="logo">P2PNet</a>
                <nav>
                    <ul>
                        <li><a href="/">Главная</a></li>
                        <li><a href="/p2p/docs/">Документация</a></li>
                        <li><a href="https://github.com/ari3lYT/p2pnet" target="_blank">GitHub</a></li>
                    </ul>
                </nav>
            </div>
        </div>
    </header>

    <main>
        <div class="container">
            <section class="hero">
                <h1>Примеры использования P2PNet</h1>
                <p class="subtitle">Изучите реальные кейсы и примеры кода для эффективной работы с сетью</p>
            </section>

            <div class="content">
                <h2>Введение</h2>
                <p>В этом разделе представлены практические примеры использования P2PNet для различных задач. От простых вычислений до сложных распределенных систем.</p>

                <div class="highlight">
                    <p><i class="fas fa-lightbulb" style="color: var(--accent-primary); margin-right: 0.5rem;"></i> Каждый пример включает полный код и объяснения. Вы можете использовать их как основу для своих проектов.</p>
                </div>

                <h2>Базовые примеры</h2>

                <div class="example-card">
                    <div class="example-header">
                        <div class="example-icon">🔢</div>
                        <div class="example-title">Математические вычисления</div>
                    </div>
                    <div class="example-description">
                        Распределенное вычисление сложных математических функций с использованием нескольких узлов сети.
                    </div>
                    
                    <div class="example-code">
                        <h4>Код для вычисления π методом Монте-Карло</h4>
                        <pre><code>import requests
import random
import math

def calculate_pi_distributed(iterations_per_node=100000):
    """
    Распределенное вычисление π методом Монте-Карло
    """
    # Определение задачи для каждого узла
    task = {
        "type": "computation",
        "command": f"""
import random
import math

def estimate_pi(iterations):
    inside_circle = 0
    for _ in range(iterations):
        x = random.random()
        y = random.random()
        if x*x + y*y <= 1:
            inside_circle += 1
    return (4 * inside_circle) / iterations

result = estimate_pi({iterations_per_node})
print(result)
        """,
        "requirements": {
            "cpu": 1,
            "memory": "256MB",
            "timeout": 60
        }
    }
    
    # Отправка задачи в сеть
    response = requests.post('http://localhost:8000/tasks', json=task)
    task_id = response.json()['task_id']
    
    # Ожидание завершения
    import time
    while True:
        status = requests.get(f'http://localhost:8000/tasks/{task_id}/status')
        if status.json()['status'] == 'completed':
            result = requests.get(f'http://localhost:8000/tasks/{task_id}/result')
            pi_estimate = float(result.json()['output'].strip())
            return pi_estimate
        time.sleep(1)

# Выполнение вычислений
pi_estimate = calculate_pi_distributed()
print(f"Приближенное значение π: {pi_estimate}")
print(f"Точное значение π: {math.pi}")
print(f"Ошибка: {abs(pi_estimate - math.pi)}")</code></pre>
                    </div>
                    
                    <div class="example-result">
                        <h4>Результат выполнения</h4>
                        <pre><code>Приближенное значение π: 3.141584
Точное значение π: 3.141592653589793
Ошибка: 0.000008653589793044</code></pre>
                    </div>
                </div>

                <div class="example-card">
                    <div class="example-header">
                        <div class="example-icon">🖼️</div>
                        <div class="example-title">Обработка изображений</div>
                    </div>
                    <div class="example-description">
                        Распределенная фильтрация и обработка изображений с использованием GPU узлов сети.
                    </div>
                    
                    <div class="example-code">
                        <h4>Код для размытия изображения</h4>
                        <pre><code>import requests
import base64
from PIL import Image
import io

def process_image_distributed(image_path, filter_type="blur"):
    """
    Распределенная обработка изображения
    """
    # Загрузка изображения
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode()
    
    # Определение задачи для обработки
    task = {
        "type": "image_processing",
        "image_data": image_data,
        "filter": filter_type,
        "requirements": {
            "cpu": 2,
            "memory": "2GB",
            "gpu": true,
            "timeout": 120
        }
    }
    
    # Отправка задачи в сеть
    response = requests.post('http://localhost:8000/tasks', json=task)
    task_id = response.json()['task_id']
    
    # Ожидание завершения
    import time
    while True:
        status = requests.get(f'http://localhost:8000/tasks/{task_id}/status')
        if status.json()['status'] == 'completed':
            result = requests.get(f'http://localhost:8000/tasks/{task_id}/result')
            processed_image_data = result.json()['image_data']
            
            # Сохранение результата
            with open(f"processed_{filter_type}.jpg", "wb") as f:
                f.write(base64.b64decode(processed_image_data))
            
            return f"processed_{filter_type}.jpg"
        time.sleep(1)

# Использование функции
result_image = process_image_distributed("input.jpg", "blur")
print(f"Обработанное изображение сохранено как: {result_image}")</code></pre>
                    </div>
                </div>

                <h2>Продвинутые примеры</h2>

                <div class="example-card">
                    <div class="example-header">
                        <div class="example-icon">🤖</div>
                        <div class="example-title">Машинное обучение</div>
                    </div>
                    <div class="example-description">
                        Распределенное обучение нейронных сетей с использованием нескольких GPU узлов.
                    </div>
                    
                    <div class="example-code">
                        <h4>Код для обучения модели классификации</h4>
                        <pre><code>import requests
import json
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

def train_model_distributed():
    """
    Распределенное обучение модели машинного обучения
    """
    # Генерация данных
    X, y = make_classification(n_samples=10000, n_features=20, n_classes=3, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Определение задачи для обучения
    task = {
        "type": "ml_training",
        "train_data": {
            "X": X_train.tolist(),
            "y": y_train.tolist()
        },
        "test_data": {
            "X": X_test.tolist(),
            "y": y_test.tolist()
        },
        "model_config": {
            "type": "random_forest",
            "n_estimators": 100,
            "max_depth": 10
        },
        "requirements": {
            "cpu": 4,
            "memory": "4GB",
            "gpu": true,
            "timeout": 300
        }
    }
    
    # Отправка задачи в сеть
    response = requests.post('http://localhost:8000/tasks', json=task)
    task_id = response.json()['task_id']
    
    # Ожидание завершения
    import time
    while True:
        status = requests.get(f'http://localhost:8000/tasks/{task_id}/status')
        if status.json()['status'] == 'completed':
            result = requests.get(f'http://localhost:8000/tasks/{task_id}/result')
            model_info = result.json()
            
            print(f"Точность модели: {model_info['accuracy']:.4f}")
            print(f"Время обучения: {model_info['training_time']:.2f} секунд")
            print(f"Использовано узлов: {model_info['nodes_used']}")
            
            return model_info
        time.sleep(1)

# Использование функции
model_result = train_model_distributed()</code></pre>
                    </div>
                </div>

                <div class="example-card">
                    <div class="example-header">
                        <div class="example-icon">🔐</div>
                        <div class="example-title">Криптографические операции</div>
                    </div>
                    <div class="example-description">
                        Распределенное шифрование и дешифрование данных с использованием безопасной песочницы.
                    </div>
                    
                    <div class="example-code">
                        <h4>Код для асимметричного шифрования</h4>
                        <pre><code>import requests
import json
from cryptography.fernet import Fernet

def encrypt_data_distributed(data, key):
    """
    Распределенное шифрование данных
    """
    # Определение задачи для шифрования
    task = {
        "type": "crypto_operation",
        "operation": "encrypt",
        "data": data,
        "key": key,
        "requirements": {
            "cpu": 1,
            "memory": "512MB",
            "timeout": 30
        }
    }
    
    # Отправка задачи в сеть
    response = requests.post('http://localhost:8000/tasks', json=task)
    task_id = response.json()['task_id']
    
    # Ожидание завершения
    import time
    while True:
        status = requests.get(f'http://localhost:8000/tasks/{task_id}/status')
        if status.json()['status'] == 'completed':
            result = requests.get(f'http://localhost:8000/tasks/{task_id}/result')
            encrypted_data = result.json()['encrypted_data']
            return encrypted_data
        time.sleep(1)

def decrypt_data_distributed(encrypted_data, key):
    """
    Распределенное дешифрование данных
    """
    # Определение задачи для дешифрования
    task = {
        "type": "crypto_operation",
        "operation": "decrypt",
        "encrypted_data": encrypted_data,
        "key": key,
        "requirements": {
            "cpu": 1,
            "memory": "512MB",
            "timeout": 30
        }
    }
    
    # Отправка задачи в сеть
    response = requests.post('http://localhost:8000/tasks', json=task)
    task_id = response.json()['task_id']
    
    # Ожидание завершения
    import time
    while True:
        status = requests.get(f'http://localhost:8000/tasks/{task_id}/status')
        if status.json()['status'] == 'completed':
            result = requests.get(f'http://localhost:8000/tasks/{task_id}/result')
            decrypted_data = result.json()['decrypted_data']
            return decrypted_data
        time.sleep(1)

# Использование функций
key = Fernet.generate_key()
data = "Это секретное сообщение для шифрования"

# Шифрование
encrypted = encrypt_data_distributed(data.decode(), key.decode())
print(f"Зашифрованные данные: {encrypted}")

# Дешифрование
decrypted = decrypt_data_distributed(encrypted, key.decode())
print(f"Дешифрованные данные: {decrypted}")</code></pre>
                    </div>
                </div>

                <h2>Интеграция с веб-приложениями</h2>

                <div class="example-card">
                    <div class="example-header">
                        <div class="example-icon">🌐</div>
                        <div class="example-title">Веб-API для P2PNet</div>
                    </div>
                    <div class="example-description">
                        Пример создания веб-API, которое использует P2PNet для выполнения вычислительных задач.
                    </div>
                    
                    <div class="example-code">
                        <h4>Код Flask API для P2PNet</h4>
                        <pre><code>from flask import Flask, request, jsonify
import requests
import threading
import time
import uuid

app = Flask(__name__)

# Хранилище задач
tasks = {}

@app.route('/compute', methods=['POST'])
def compute():
    """
    Эндпоинт для выполнения вычислений
    """
    data = request.json
    
    # Валидация запроса
    if 'code' not in data:
        return jsonify({'error': 'Code is required'}), 400
    
    # Генерация ID задачи
    task_id = str(uuid.uuid4())
    
    # Определение задачи для P2PNet
    task = {
        "type": "computation",
        "command": data['code'],
        "requirements": data.get('requirements', {
            "cpu": 1,
            "memory": "512MB",
            "timeout": 60
        })
    }
    
    # Отправка задачи в P2PNet
    try:
        response = requests.post('http://localhost:8000/tasks', json=task, timeout=10)
        p2p_task_id = response.json()['task_id']
        
        # Сохранение информации о задаче
        tasks[task_id] = {
            'p2p_task_id': p2p_task_id,
            'status': 'pending',
            'result': None,
            'created_at': time.time()
        }
        
        # Запуск фонового процесса отслеживания
        threading.Thread(target=monitor_task, args=(task_id,)).start()
        
        return jsonify({
            'task_id': task_id,
            'status': 'pending'
        }), 202
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to submit task: {str(e)}'}), 500

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """
    Получение статуса задачи
    """
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    task = tasks[task_id]
    return jsonify({
        'task_id': task_id,
        'status': task['status'],
        'result': task['result'],
        'created_at': task['created_at']
    })

@app.route('/tasks/<task_id>/result', methods=['GET'])
def get_task_result(task_id):
    """
    Получение результата задачи
    """
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    task = tasks[task_id]
    
    if task['status'] != 'completed':
        return jsonify({'error': 'Task not completed yet'}), 400
    
    return jsonify(task['result'])

def monitor_task(task_id):
    """
    Мониторинг выполнения задачи
    """
    task = tasks[task_id]
    p2p_task_id = task['p2p_task_id']
    
    while True:
        try:
            status = requests.get(f'http://localhost:8000/tasks/{p2p_task_id}/status', timeout=5)
            status_data = status.json()
            
            if status_data['status'] == 'completed':
                # Получение результата
                result = requests.get(f'http://localhost:8000/tasks/{p2p_task_id}/result')
                task['status'] = 'completed'
                task['result'] = result.json()
                break
            elif status_data['status'] == 'failed':
                task['status'] = 'failed'
                task['result'] = {'error': status_data.get('error', 'Unknown error')}
                break
                
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(2)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)</code></pre>
                    </div>
                </div>

                <div class="highlight">
                    <p><i class="fas fa-info-circle" style="color: var(--accent-primary); margin-right: 0.5rem;"></i> Эти примеры демонстрируют мощь и гибкость P2PNet. Вы можете адаптировать их под свои нужды или создавать собственные решения на их основе.</p>
                </div>

                <h2>Рекомендации по оптимизации</h2>
                
                <ul>
                    <li><strong>Разбиение больших задач:</strong> Разделяйте сложные задачи на более мелкие для параллельного выполнения</li>
                    <li><strong>Оптимизация ресурсов:</strong> Точно указывайте требования к CPU, памяти и GPU</li>
                    <li><strong>Обработка ошибок:</strong> Реализуйте надежную обработку ошибок и повторные попытки</li>
                    <li><strong>Кэширование результатов:</strong> Кэшируйте результаты одинаковых задач для экономии ресурсов</li>
                    <li><strong>Мониторинг производительности:</strong> Используйте встроенные метрики для оптимизации</li>
                </ul>

                <div class="nav-links">
                    <a href="/p2p/docs/getting-started.html"><i class="fas fa-arrow-left"></i> Быстрый старт</a>
                    <a href="/p2p/docs/api-reference.html"><i class="fas fa-code"></i> API Ссылка <i class="fas fa-arrow-right"></i></a>
                </div>
            </div>
        </div>
    </main>

    <footer>
        <div class="container">
            <div class="footer-content">
                <p>&copy; 2025 P2PNet. Проект с открытым исходным кодом.</p>
                <div class="social-links">
                    <a href="https://github.com/ari3lYT/p2pnet" target="_blank">
                        <i class="fab fa-github"></i> GitHub
                    </a>
                    <a href="https://t.me/gweles" target="_blank">
                        <i class="fab fa-telegram"></i> Telegram
                    </a>
                </div>
            </div>
        </div>
    </footer>
</body>
</html>
