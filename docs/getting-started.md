<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Быстрый старт - P2PNet</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --bg-primary: #ffffff;
            --bg-secondary: #f8f9fa;
            --bg-tertiary: #e9ecef;
            --text-primary: #212529;
            --text-secondary: #6c757d;
            --text-muted: #adb5bd;
            --accent-primary: #0066cc;
            --accent-secondary: #0052a3;
            --border-color: #dee2e6;
            --gradient-primary: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: var(--text-primary);
            background-color: var(--bg-primary);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        header {
            background-color: var(--bg-primary);
            border-bottom: 1px solid var(--border-color);
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 1000;
            transition: all 0.3s ease;
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
            transition: color 0.3s ease;
        }

        .logo:hover {
            color: var(--accent-primary);
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
            transition: color 0.3s ease;
        }

        nav a:hover {
            color: var(--accent-primary);
        }

        main {
            padding-top: 80px;
            min-height: 100vh;
        }

        .hero {
            padding: 4rem 0;
            text-align: center;
            background: var(--bg-secondary);
        }

        .hero h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }

        .hero .subtitle {
            font-size: 1.25rem;
            color: var(--text-secondary);
            max-width: 600px;
            margin: 0 auto 2rem;
        }

        .content {
            padding: 3rem 0;
        }

        .content h2 {
            font-size: 2rem;
            margin-bottom: 1.5rem;
            color: var(--text-primary);
            font-weight: 700;
        }

        .content h3 {
            font-size: 1.5rem;
            margin: 2rem 0 1rem 0;
            color: var(--text-primary);
            font-weight: 600;
        }

        .content h4 {
            font-size: 1.25rem;
            margin: 1.5rem 0 0.75rem 0;
            color: var(--text-primary);
            font-weight: 600;
        }

        .content p {
            color: var(--text-secondary);
            margin-bottom: 1rem;
            line-height: 1.6;
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
            background: var(--bg-secondary);
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid var(--accent-primary);
            margin: 1.5rem 0;
        }

        .content .highlight p {
            color: var(--text-primary);
            margin-bottom: 0;
        }

        .step-card {
            background: var(--bg-secondary);
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            margin: 2rem 0;
            position: relative;
            transition: all 0.3s ease;
        }

        .step-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        .step-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--gradient-primary);
            border-radius: 3px 3px 0 0;
        }

        .step-number {
            display: inline-block;
            background: var(--gradient-primary);
            color: white;
            width: 2.5rem;
            height: 2.5rem;
            border-radius: 50%;
            text-align: center;
            line-height: 2.5rem;
            font-weight: bold;
            margin-right: 1rem;
            font-size: 1.1rem;
        }

        .requirements {
            background: var(--bg-secondary);
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            margin: 2rem 0;
        }

        .requirements h4 {
            color: var(--accent-primary);
            margin-bottom: 1.5rem;
            font-size: 1.25rem;
            font-weight: 600;
        }

        .requirements ul {
            margin-left: 1rem;
        }

        .requirements li {
            margin-bottom: 0.75rem;
            color: var(--text-secondary);
            font-size: 1rem;
        }

        .requirements .requirement-group {
            margin-bottom: 1.5rem;
        }

        .requirements .requirement-group h5 {
            color: var(--text-primary);
            margin-bottom: 0.75rem;
            font-size: 1.1rem;
            font-weight: 600;
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
            font-weight: 600;
            transition: color 0.3s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .nav-links a:hover {
            color: var(--accent-secondary);
        }

        .nav-links i {
            font-size: 1.1rem;
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
            transition: color 0.3s ease;
        }

        .social-links a:hover {
            color: var(--accent-primary);
        }

        @media (max-width: 768px) {
            nav ul {
                gap: 1rem;
            }
            
            .hero h1 {
                font-size: 2rem;
            }
            
            .hero .subtitle {
                font-size: 1.1rem;
            }
            
            .content {
                padding: 2rem 0;
            }
            
            .step-card {
                padding: 1.5rem;
                margin: 1.5rem 0;
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
                <h1>Быстрый старт с P2PNet</h1>
                <p class="subtitle">За 5 минут вы запустите свой первый узел в децентрализованной сети</p>
            </section>

            <section class="content">
                <div class="container">
                    <div class="highlight">
                        <p><i class="fas fa-rocket" style="color: var(--accent-primary); margin-right: 0.5rem;"></i> Весь процесс занимает не более 5 минут. Готовы начать?</p>
                    </div>

                    <h2>Введение</h2>
                    <p>Это руководство проведет вас через процесс установки, настройки и запуска вашего первого узла в сети P2PNet. Вы сможете предоставлять вычислительные ресурсы или использовать сеть для выполнения задач.</p>

                    <div class="requirements">
                        <h4>Требования системы</h4>
                        
                        <div class="requirement-group">
                            <h5>Минимальные требования</h5>
                            <ul>
                                <li>Операционная система: Linux, macOS или Windows</li>
                                <li>Python 3.11 или выше</li>
                                <li>Доступ в интернет</li>
                                <li>Минимум 2 ГБ оперативной памяти</li>
                                <li>Минимум 1 ГБ свободного места на диске</li>
                            </ul>
                        </div>

                        <div class="requirement-group">
                            <h5>Рекомендуемые требования</h5>
                            <ul>
                                <li>4+ ядра процессора</li>
                                <li>8+ ГБ оперативной памяти</li>
                                <li>SSD накопитель</li>
                                <li>Стабильное интернет-соединение</li>
                                <li>Опционально: GPU для ML задач</li>
                            </ul>
                        </div>
                    </div>

                    <h2>Установка</h2>
                    
                    <div class="step-card">
                        <h3><span class="step-number">1</span>Клонирование репозитория</h3>
                        <p>Сначала скачайте исходный код P2PNet с GitHub:</p>
                        
                        <pre><code>git clone https://github.com/ari3lYT/p2pnet.git
cd p2pnet</code></pre>
                    </div>

                    <div class="step-card">
                        <h3><span class="step-number">2</span>Установка зависимостей</h3>
                        <p>Установите все необходимые Python пакеты:</p>
                        
                        <pre><code>pip install -r requirements.txt</code></pre>
                        
                        <p>Если вы используете Python 3.11+, рекомендуется создать виртуальное окружение:</p>
                        
                        <pre><code>python -m venv p2pnet-env
source p2pnet-env/bin/activate  # Для Linux/macOS
# или
p2pnet-env\Scripts\activate     # Для Windows
pip install -r requirements.txt</code></pre>
                    </div>

                    <div class="step-card">
                        <h3><span class="step-number">3</span>Настройка конфигурации</h3>
                        <p>Создайте конфигурационный файл для вашего узла:</p>
                        
                        <pre><code>{
  "version": 1,
  "node_id": "my-computer-001",
  "host": "0.0.0.0",
  "port": 5555,
  "sandbox": {
    "type": "process_isolation",
    "resource_limits": {
      "cpu_time_seconds": 30,
      "memory_bytes": 104857600,
      "file_size_bytes": 52428800
    }
  },
  "pricing": {
    "base_cpu_price": 0.01,
    "base_gpu_price": 0.05,
    "base_ram_price": 0.02
  },
  "network": {
    "discovery_port": 5556,
    "max_peers": 100,
    "bootstrap_hosts": [
      "127.0.0.1:5555"
    ]
  }
}</code></pre>
                        
                        <div class="highlight">
                            <p><i class="fas fa-info-circle" style="color: var(--accent-primary); margin-right: 0.5rem;"></i> Замените <code>my-computer-001</code> на уникальный идентификатор для вашего узла. Это поможет другим участникам сети идентифицировать ваш узел.</p>
                        </div>
                    </div>

                    <div class="step-card">
                        <h3><span class="step-number">4</span>Запуск узла</h3>
                        <p>Запустите ваш узел в сети:</p>
                        
                        <pre><code>python src/main.py --config config.json</code></pre>
                        
                        <p>После запуска вы увидите логи подключения к сети:</p>
                        
                        <pre><code>🚀 Вычислительный узел запущен на 0.0.0.0:5555
🆔 Node ID: abc123...
💪 Возможности: CPU=2450, GPU=0, RAM=16.0GB
🔗 Подключено к сети</code></pre>
                    </div>

                    <div class="step-card">
                        <h3><span class="step-number">5</span>Проверка работы</h3>
                        <p>Убедитесь, что ваш узел работает корректно:</p>
                        
                        <pre><code>curl http://localhost:5555/status</code></pre>
                        
                        <p>Вы должны увидеть ответ в формате JSON:</p>
                        
                        <pre><code>{
  "node_id": "abc123...",
  "status": "active",
  "capabilities": {
    "cpu_score": 2450,
    "gpu_score": 0,
    "ram_gb": 16.0,
    "cpu_usage": 15.2,
    "ram_usage": 45.8
  },
  "peers_count": 5,
  "active_tasks": 0,
  "credits": 0.0
}</code></pre>
                    </div>

                    <h2>Первая задача</h2>
                    
                    <p>Теперь, когда ваш узел запущен, вы можете отправить первую задачу в сеть:</p>
                    
                    <h3>Пример простой задачи</h3>
                    
                    <pre><code>import asyncio
from src.main import ComputeNetwork
from src.core.task import Task

async def main():
    # Создаем сеть
    network = ComputeNetwork(host='127.0.0.1', port=5556)
    await network.start()
    
    # Создаем задачу
    task = Task.create_range_reduce(
        owner_id=network.node.node_id,
        start=1,
        end=1000,
        operation="sum",
        requirements={
            "cpu_percent": 50.0,
            "ram_gb": 0.5,
            "timeout_seconds": 30
        },
        config={
            "max_price": 0.1,
            "priority": "normal"
        }
    )
    
    # Подаем задачу
    task_id = await network.submit_task(task.to_dict())
    print(f"✅ Задача создана: {task_id}")
    
    # Ожидание завершения
    import time
    while True:
        status = await network.get_task_status(task_id)
        if status['status'] == 'completed':
            print("Результат:", status['result'])
            break
        time.sleep(1)
    
    await network.stop()

asyncio.run(main())</code></pre>

                    <div class="highlight">
                        <p><i class="fas fa-check-circle" style="color: var(--accent-primary); margin-right: 0.5rem;"></i> Поздравляем! Вы успешно запустили свой узел и выполнили первую задачу в сети P2PNet.</p>
                    </div>

                    <h2>Дальнейшие шаги</h2>
                    
                    <h3>1. Оптимизация производительности</h3>
                    <ul>
                        <li>Настройте количество выделяемых CPU ядер</li>
                        <li>Оптимизируйте использование памяти</li>
                        <li>Включите мониторинг для отслеживания производительности</li>
                        <li>Настройте динамическое ценообразование</li>
                    </ul>

                    <h3>2. Безопасность</h3>
                    <ul>
                        <li>Используйте HTTPS для защищенной коммуникации</li>
                        <li>Настройте брандмауэр</li>
                        <li>Регулярно обновляйте систему</li>
                        <li>Настройте ограничения ресурсов в sandbox</li>
                    </ul>

                    <h3>3. Мониторинг</h3>
                    <ul>
                        <li>Настраивайте логирование</li>
                        <li>Используйте встроенные метрики</li>
                        <li>Интегрируйте с системами мониторинга</li>
                        <li>Следите за репутацией вашего узла</li>
                    </ul>

                    <h3>4. Интеграция</h3>
                    <ul>
                        <li>Изучите API для интеграции с вашими приложениями</li>
                        <li>Создайте сложные pipeline задачи</li>
                        <li>Интегрируйте ML модели в сеть</li>
                        <li>Настройте автоматическое масштабирование</li>
                    </ul>

                    <div class="nav-links">
                        <a href="/p2p/docs/"><i class="fas fa-arrow-left"></i> Вернуться к документации</a>
                        <a href="/p2p/docs/examples.html"><i class="fas fa-laptop-code"></i> Примеры использования <i class="fas fa-arrow-right"></i></a>
                    </div>
                </div>
            </section>
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
