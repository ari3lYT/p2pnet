<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Документация - P2PNet</title>
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

        .toc {
            background: var(--bg-secondary);
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            margin: 2rem 0;
        }

        .toc h3 {
            color: var(--text-primary);
            margin-bottom: 1.5rem;
            font-size: 1.3rem;
            font-weight: 600;
        }

        .toc ul {
            list-style: none;
            margin-left: 0;
        }

        .toc li {
            margin-bottom: 1rem;
        }

        .toc a {
            color: var(--text-secondary);
            text-decoration: none;
            transition: color 0.3s ease;
            display: flex;
            align-items: center;
            font-weight: 500;
        }

        .toc a:hover {
            color: var(--accent-primary);
        }

        .toc i {
            margin-right: 0.75rem;
            color: var(--accent-primary);
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }

        .feature-card {
            background: var(--bg-secondary);
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
        }

        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        .feature-card h4 {
            font-size: 1.25rem;
            margin-bottom: 1rem;
            color: var(--text-primary);
            font-weight: 600;
        }

        .feature-card p {
            color: var(--text-secondary);
            line-height: 1.6;
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
            
            .toc {
                padding: 1.5rem;
            }
            
            .feature-grid {
                grid-template-columns: 1fr;
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
                        <li><a href="https://github.com/ari3lYT/p2pnet" target="_blank">GitHub</a></li>
                    </ul>
                </nav>
            </div>
        </div>
    </header>

    <main>
        <div class="container">
            <section class="hero">
                <h1>Документация P2PNet</h1>
                <p class="subtitle">Полное руководство по использованию децентрализованной сети вычислений</p>
            </section>

            <section class="content">
                <div class="container">
                    <div class="highlight">
                        <p><i class="fas fa-info-circle" style="color: var(--accent-primary); margin-right: 0.5rem;"></i> P2PNet - это проект с открытым исходным кодом. Вы можете изучить код, внести свой вклад или использовать платформу для своих задач.</p>
                    </div>

                    <h2>Введение</h2>
                    <p>P2PNet - это современная платформа для распределенных вычислений, построенная на принципах децентрализации. Сеть позволяет пользователям обмениваться вычислительными ресурсами без посредников, используя compute-кредиты для учета ресурсов.</p>

                    <h3>Ключевые особенности</h3>
                    <div class="feature-grid">
                        <div class="feature-card">
                            <h4><i class="fas fa-network-wired"></i> Децентрализация</h4>
                            <p>Нет единого центра управления. Каждый узел является равноправным участником сети.</p>
                        </div>
                        <div class="feature-card">
                            <h4><i class="fas fa-coins"></i> Compute-кредиты</h4>
                            <p>Система учета ресурсов без денег. Кредиты начисляются за выполнение задач.</p>
                        </div>
                        <div class="feature-card">
                            <h4><i class="fas fa-shield-alt"></i> Безопасность</h4>
                            <p>Sandbox изоляция для безопасного выполнения кода с криптографическими подписями.</p>
                        </div>
                        <div class="feature-card">
                            <h4><i class="fas fa-brain"></i> ML/AI поддержка</h4>
                            <p>Оптимизированная работа с машинным обучением и нейронными сетями.</p>
                        </div>
                        <div class="feature-card">
                            <h4><i class="fas fa-chart-line"></i> Динамическое ценообразование</h4>
                            <p>Адаптивные цены на основе спроса, предложения и репутации узлов.</p>
                        </div>
                        <div class="feature-card">
                            <h4><i class="fas fa-expand-arrows-alt"></i> Масштабируемость</h4>
                            <p>Горизонтальное масштабирование от одного узла до тысяч.</p>
                        </div>
                    </div>

                    <h2>Структура документации</h2>
                    
                    <div class="toc">
                        <h3>Содержание</h3>
                        <ul>
                            <li><a href="/p2p/docs/getting-started.html"><i class="fas fa-rocket"></i> Быстрый старт</a></li>
                            <li><a href="/p2p/docs/ARCHITECTURE_OVERVIEW.html"><i class="fas fa-sitemap"></i> Архитектура сети</a></li>
                            <li><a href="/p2p/docs/api-reference.html"><i class="fas fa-code"></i> API Ссылка</a></li>
                            <li><a href="/p2p/docs/examples.html"><i class="fas fa-laptop-code"></i> Примеры использования</a></li>
                            <li><a href="/p2p/docs/deployment.html"><i class="fas fa-server"></i> Развертывание</a></li>
                            <li><a href="/p2p/docs/security.html"><i class="fas fa-shield-alt"></i> Безопасность</a></li>
                        </ul>
                    </div>

                    <h2>Типы задач</h2>
                    <p>Система поддерживает различные типы вычислительных задач:</p>
                    
                    <ul>
                        <li><strong>Базовые операции:</strong> range_reduce, map, map_reduce, matrix_ops</li>
                        <li><strong>ML/AI задачи:</strong> ml_inference, ml_train_step</li>
                        <li><strong>Универсальные задачи:</strong> generic с поддержкой builtin, python_script, wasm, container</li>
                        <li><strong>Сложные пайплайны:</strong> pipeline с DAG зависимостями</li>
                    </ul>

                    <h2>Пример использования</h2>
                    
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
        }
    )
    
    # Подаем задачу
    task_id = await network.submit_task(task.to_dict())
    print(f"✅ Задача создана: {task_id}")
    
    await network.stop()

asyncio.run(main())</code></pre>

                    <div class="highlight">
                        <p><i class="fas fa-lightbulb" style="color: var(--accent-primary); margin-right: 0.5rem;"></i> Больше примеров и подробных инструкций доступно в соответствующих разделах документации.</p>
                    </div>

                    <h2>Начало работы</h2>
                    <p>Чтобы начать работу с P2PNet:</p>
                    
                    <ol>
                        <li>Установите Python 3.11+ и необходимые зависимости</li>
                        <li>Клонируйте репозиторий с GitHub</li>
                        <li>Настройте конфигурационный файл для вашего узла</li>
                        <li>Запустите узел сети</li>
                        <li>Начните отправлять задачи или предоставлять вычислительные ресурсы</li>
                    </ol>

                    <div class="nav-links">
                        <a href="/"><i class="fas fa-arrow-left"></i> Вернуться на главную</a>
                        <a href="/p2p/docs/getting-started.html"><i class="fas fa-rocket"></i> Начать работу <i class="fas fa-arrow-right"></i></a>
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