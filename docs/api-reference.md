<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Ссылка - P2PNet</title>
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

        .api-section {
            background: var(--bg-tertiary);
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            margin: 2rem 0;
        }

        .api-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: var(--gradient-primary);
        }

        .method-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            margin-right: 0.5rem;
        }

        .method-get {
            background: rgba(0, 212, 255, 0.1);
            color: var(--accent-primary);
            border: 1px solid var(--accent-primary);
        }

        .method-post {
            background: rgba(0, 255, 128, 0.1);
            color: #00ff80;
            border: 1px solid #00ff80;
        }

        .method-put {
            background: rgba(255, 193, 7, 0.1);
            color: #ffc107;
            border: 1px solid #ffc107;
        }

        .method-delete {
            background: rgba(220, 53, 69, 0.1);
            color: #dc3545;
            border: 1px solid #dc3545;
        }

        .endpoint {
            color: var(--accent-primary);
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 1rem;
        }

        .parameter-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }

        .parameter-table th,
        .parameter-table td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }

        .parameter-table th {
            background: var(--bg-secondary);
            color: var(--text-primary);
            font-weight: 600;
        }

        .parameter-table td {
            color: var(--text-secondary);
        }

        .parameter-table code {
            background: var(--bg-secondary);
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            color: var(--accent-primary);
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.9rem;
        }

        .response-example {
            background: var(--bg-secondary);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            margin: 1rem 0;
        }

        .response-example h4 {
            color: var(--accent-primary);
            margin-bottom: 0.5rem;
            font-size: 1rem;
        }

        .response-example pre {
            background: var(--bg-tertiary);
            padding: 1rem;
            border-radius: 4px;
            margin: 0;
            font-size: 0.9rem;
        }

        .toc {
            background: var(--bg-tertiary);
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            margin: 2rem 0;
            position: sticky;
            top: 100px;
        }

        .toc h3 {
            color: var(--text-primary);
            margin-bottom: 1rem;
            font-size: 1.3rem;
        }

        .toc ul {
            list-style: none;
            margin-left: 0;
        }

        .toc li {
            margin-bottom: 0.75rem;
        }

        .toc a {
            color: var(--text-secondary);
            text-decoration: none;
            transition: color 0.3s ease;
            display: flex;
            align-items: center;
        }

        .toc a:hover {
            color: var(--accent-primary);
        }

        .toc a i {
            margin-right: 0.5rem;
            width: 1rem;
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
            
            .api-section {
                padding: 1.5rem;
            }
            
            .toc {
                position: static;
                margin: 1rem 0;
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
                <h1>API Ссылка P2PNet</h1>
                <p class="subtitle">Полное описание API для интеграции с децентрализованной сетью вычислений</p>
            </section>

            <div class="content">
                <div style="display: grid; grid-template-columns: 300px 1fr; gap: 2rem;">
                    <div class="toc">
                        <h3>Содержание</h3>
                        <ul>
                            <li><a href="#overview"><i class="fas fa-info-circle"></i> Обзор</a></li>
                            <li><a href="#authentication"><i class="fas fa-key"></i> Аутентификация</a></li>
                            <li><a href="#nodes"><i class="fas fa-network-wired"></i> Управление узлами</a></li>
                            <li><a href="#tasks"><i class="fas fa-tasks"></i> Управление задачами</a></li>
                            <li><a href="#monitoring"><i class="fas fa-chart-line"></i> Мониторинг</a></li>
                            <li><a href="#payments"><i class="fas fa-coins"></i> Платежи</a></li>
                            <li><a href="#errors"><i class="fas fa-exclamation-triangle"></i> Обработка ошибок</a></li>
                        </ul>
                    </div>

                    <div>
                        <h2 id="overview">Обзор API</h2>
                        <p>P2PNet предоставляет RESTful API для взаимодействия с децентрализованной сетью вычислений. API позволяет:</p>
                        <ul>
                            <li>Регистрировать и управлять узлами сети</li>
                            <li>Публиковать и выполнять вычислительные задачи</li>
                            <li>Мониторить состояние сети и узлов</li>
                            <li>Обрабатывать платежи и транзакции</li>
                            <li>Получать статистику и метрики</li>
                        </ul>

                        <div class="highlight">
                            <p><i class="fas fa-globe" style="color: var(--accent-primary); margin-right: 0.5rem;"></i> Базовый URL: <code>http://localhost:8000</code> (замените на адрес вашего узла)</p>
                        </div>

                        <h2 id="authentication">Аутентификация</h2>
                        <p>Для большинства операций требуется аутентификация с использованием API ключа:</p>

                        <div class="api-section">
                            <h3><span class="method-badge">post</span>Получение API ключа</h3>
                            <p class="endpoint">POST /api/auth/key</p>
                            
                            <h4>Параметры запроса</h4>
                            <table class="parameter-table">
                                <thead>
                                    <tr>
                                        <th>Параметр</th>
                                        <th>Тип</th>
                                        <th>Описание</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><code>node_id</code></td>
                                        <td>string</td>
                                        <td>Уникальный идентификатор узла</td>
                                    </tr>
                                    <tr>
                                        <td><code>public_key</code></td>
                                        <td>string</td>
                                        <td>Публичный ключ для шифрования</td>
                                    </tr>
                                </tbody>
                            </table>

                            <h4>Ответ</h4>
                            <div class="response-example">
                                <h4>Успешный ответ (200 OK)</h4>
                                <pre><code>{
  "api_key": "your_api_key_here",
  "expires_at": "2025-12-31T23:59:59Z",
  "permissions": ["read", "write", "compute"]
}</code></pre>
                            </div>
                        </div>

                        <h2 id="nodes">Управление узлами</h2>

                        <div class="api-section">
                            <h3><span class="method-badge">post</span>Регистрация узла</h3>
                            <p class="endpoint">POST /api/nodes</p>
                            
                            <h4>Параметры запроса</h4>
                            <table class="parameter-table">
                                <thead>
                                    <tr>
                                        <th>Параметр</th>
                                        <th>Тип</th>
                                        <th>Описание</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><code>node_id</code></td>
                                        <td>string</td>
                                        <td>Уникальный идентификатор узла</td>
                                    </tr>
                                    <tr>
                                        <td><code>capabilities</code></td>
                                        <td>object</td>
                                        <td>Возможности узла (CPU, RAM, GPU)</td>
                                    </tr>
                                    <tr>
                                        <td><code>location</code></td>
                                        <td>object</td>
                                        <td>Географическое положение</td>
                                    </tr>
                                    <tr>
                                        <td><code>api_key</code></td>
                                        <td>string</td>
                                        <td>API ключ для аутентификации</td>
                                    </tr>
                                </tbody>
                            </table>

                            <h4>Ответ</h4>
                            <div class="response-example">
                                <h4>Успешный ответ (201 Created)</h4>
                                <pre><code>{
  "node_id": "node-123",
  "status": "registered",
  "message": "Node successfully registered",
  "endpoint": "ws://node-123:8000"
}</code></pre>
                            </div>
                        </div>

                        <div class="api-section">
                            <h3><span class="method-badge">get</span>Получение информации об узле</h3>
                            <p class="endpoint">GET /api/nodes/{node_id}</p>
                            
                            <h4>Параметры пути</h4>
                            <table class="parameter-table">
                                <thead>
                                    <tr>
                                        <th>Параметр</th>
                                        <th>Тип</th>
                                        <th>Описание</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><code>node_id</code></td>
                                        <td>string</td>
                                        <td>Идентификатор узла</td>
                                    </tr>
                                </tbody>
                            </table>

                            <h4>Ответ</h4>
                            <div class="response-example">
                                <h4>Успешный ответ (200 OK)</h4>
                                <pre><code>{
  "node_id": "node-123",
  "status": "active",
  "capabilities": {
    "cpu": 8,
    "memory": "16GB",
    "gpu": "RTX 3080",
    "storage": "500GB SSD"
  },
  "location": {
    "country": "RU",
    "city": "Moscow"
  },
  "reputation": 95,
  "uptime": 99.9,
  "last_seen": "2025-01-01T10:00:00Z"
}</code></pre>
                            </div>
                        </div>

                        <h2 id="tasks">Управление задачами</h2>

                        <div class="api-section">
                            <h3><span class="method-badge">post</span>Публикация задачи</h3>
                            <p class="endpoint">POST /api/tasks</p>
                            
                            <h4>Параметры запроса</h4>
                            <table class="parameter-table">
                                <thead>
                                    <tr>
                                        <th>Параметр</th>
                                        <th>Тип</th>
                                        <th>Описание</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><code>type</code></td>
                                        <td>string</td>
                                        <td>Тип задачи (computation, ml, etc.)</td>
                                    </tr>
                                    <tr>
                                        <td><code>command</code></td>
                                        <td>string</td>
                                        <td>Команда для выполнения</td>
                                    </tr>
                                    <tr>
                                        <td><code>requirements</code></td>
                                        <td>object</td>
                                        <td>Требования к ресурсам</td>
                                    </tr>
                                    <tr>
                                        <td><code>timeout</code></td>
                                        <td>integer</td>
                                        <td>Таймаут в секундах</td>
                                    </tr>
                                    <tr>
                                        <td><code>budget</code></td>
                                        <td>float</td>
                                        <td>Бюджет задачи в криптовалюте</td>
                                    </tr>
                                </tbody>
                            </table>

                            <h4>Ответ</h4>
                            <div class="response-example">
                                <h4>Успешный ответ (202 Accepted)</h4>
                                <pre><code>{
  "task_id": "task-456",
  "status": "pending",
  "estimated_cost": 0.001,
  "estimated_time": 30,
  "message": "Task submitted successfully"
}</code></pre>
                            </div>
                        </div>

                        <div class="api-section">
                            <h3><span class="method-badge">get</span>Получение статуса задачи</h3>
                            <p class="endpoint">GET /api/tasks/{task_id}/status</p>
                            
                            <h4>Параметры пути</h4>
                            <table class="parameter-table">
                                <thead>
                                    <tr>
                                        <th>Параметр</th>
                                        <th>Тип</th>
                                        <th>Описание</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><code>task_id</code></td>
                                        <td>string</td>
                                        <td>Идентификатор задачи</td>
                                    </tr>
                                </tbody>
                            </table>

                            <h4>Ответ</h4>
                            <div class="response-example">
                                <h4>Успешный ответ (200 OK)</h4>
                                <pre><code>{
  "task_id": "task-456",
  "status": "running",
  "progress": 65,
  "assigned_nodes": ["node-123", "node-456"],
  "started_at": "2025-01-01T10:00:00Z",
  "estimated_completion": "2025-01-01T10:00:30Z"
}</code></pre>
                            </div>
                        </div>

                        <div class="api-section">
                            <h3><span class="method-badge">get</span>Получение результата задачи</h3>
                            <p class="endpoint">GET /api/tasks/{task_id}/result</p>
                            
                            <h4>Параметры пути</h4>
                            <table class="parameter-table">
                                <thead>
                                    <tr>
                                        <th>Параметр</th>
                                        <th>Тип</th>
                                        <th>Описание</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><code>task_id</code></td>
                                        <td>string</td>
                                        <td>Идентификатор задачи</td>
                                    </tr>
                                </tbody>
                            </table>

                            <h4>Ответ</h4>
                            <div class="response-example">
                                <h4>Успешный ответ (200 OK)</h4>
                                <pre><code>{
  "task_id": "task-456",
  "status": "completed",
  "result": {
    "output": "Calculation completed successfully",
    "data": {
      "value": 42,
      "timestamp": "2025-01-01T10:00:30Z"
    }
  },
  "cost": 0.001,
  "execution_time": 28.5,
  "used_resources": {
    "cpu": 2,
    "memory": "1GB",
    "gpu": false
  }
}</code></pre>
                            </div>
                        </div>

                        <h2 id="monitoring">Мониторинг</h2>

                        <div class="api-section">
                            <h3><span class="method-badge">get</span>Получение статистики сети</h3>
                            <p class="endpoint">GET /api/stats/network</p>
                            
                            <h4>Ответ</h4>
                            <div class="response-example">
                                <h4>Успешный ответ (200 OK)</h4>
                                <pre><code>{
  "total_nodes": 150,
  "active_nodes": 142,
  "total_tasks": 1000,
  "active_tasks": 25,
  "average_uptime": 99.5,
  "total_computing_power": {
    "cpu": 1200,
    "memory": "2TB",
    "gpu": 45
  },
  "network_load": 0.65,
  "last_updated": "2025-01-01T10:00:00Z"
}</code></pre>
                            </div>
                        </div>

                        <div class="api-section">
                            <h3><span class="method-badge">get</span>Получение метрик узла</h3>
                            <p class="endpoint">GET /api/nodes/{node_id}/metrics</p>
                            
                            <h4>Параметры пути</h4>
                            <table class="parameter-table">
                                <thead>
                                    <tr>
                                        <th>Параметр</th>
                                        <th>Тип</th>
                                        <th>Описание</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><code>node_id</code></td>
                                        <td>string</td>
                                        <td>Идентификатор узла</td>
                                    </tr>
                                </tbody>
                            </table>

                            <h4>Ответ</h4>
                            <div class="response-example">
                                <h4>Успешный ответ (200 OK)</h4>
                                <pre><code>{
  "node_id": "node-123",
  "metrics": {
    "cpu_usage": 45.2,
    "memory_usage": "8.2GB/16GB",
    "disk_usage": "120GB/500GB",
    "network_in": 1.2,
    "network_out": 0.8,
    "temperature": 65,
    "uptime": 99.9
  },
  "timestamp": "2025-01-01T10:00:00Z"
}</code></pre>
                            </div>
                        </div>

                        <h2 id="payments">Платежи</h2>

                        <div class="api-section">
                            <h3><span class="method-badge">post</span>Инициализация платежа</h3>
                            <p class="endpoint">POST /api/payments/initiate</p>
                            
                            <h4>Параметры запроса</h4>
                            <table class="parameter-table">
                                <thead>
                                    <tr>
                                        <th>Параметр</th>
                                        <th>Тип</th>
                                        <th>Описание</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><code>task_id</code></td>
                                        <td>string</td>
                                        <td>Идентификатор задачи</td>
                                    </tr>
                                    <tr>
                                        <td><code>amount</code></td>
                                        <td>float</td>
                                        <td>Сумма платежа</td>
                                    </tr>
                                    <tr>
                                        <td><code>currency</code></td>
                                        <td>string</td>
                                        <td>Криптовалюта (BTC, ETH, etc.)</td>
                                    </tr>
                                    <tr>
                                        <td><code>recipient_address</code></td>
                                        <td>string</td>
                                        <td>Адрес получателя</td>
                                    </tr>
                                </tbody>
                            </table>

                            <h4>Ответ</h4>
                            <div class="response-example">
                                <h4>Успешный ответ (200 OK)</h4>
                                <pre><code>{
  "payment_id": "payment-789",
  "status": "pending",
  "amount": 0.001,
  "currency": "ETH",
  "transaction_hash": "0x123...abc",
  "estimated_fee": 0.0001,
  "total_amount": 0.0011
}</code></pre>
                            </div>
                        </div>

                        <h2 id="errors">Обработка ошибок</h2>
                        <p>API возвращает стандартные HTTP коды статуса и сообщения об ошибках в формате JSON:</p>

                        <div class="api-section">
                            <h4>Коды ошибок</h4>
                            <table class="parameter-table">
                                <thead>
                                    <tr>
                                        <th>Код</th>
                                        <th>Описание</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>400</td>
                                        <td>Неверный запрос</td>
                                    </tr>
                                    <tr>
                                        <td>401</td>
                                        <td>Неавторизован</td>
                                    </tr>
                                    <tr>
                                        <td>403</td>
                                        <td>Доступ запрещен</td>
                                    </tr>
                                    <tr>
                                        <td>404</td>
                                        <td>Не найдено</td>
                                    </tr>
                                    <tr>
                                        <td>429</td>
                                        <td>Слишком много запросов</td>
                                    </tr>
                                    <tr>
                                        <td>500</td>
                                        <td>Внутренняя ошибка сервера</td>
                                    </tr>
                                    <tr>
                                        <td>503</td>
                                        <td>Сервис недоступен</td>
                                    </tr>
                                </tbody>
                            </table>

                            <h4>Формат ошибки</h4>
                            <div class="response-example">
                                <h4>Пример ответа об ошибке</h4>
                                <pre><code>{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid task requirements",
    "details": "Memory requirement must be specified"
  },
  "request_id": "req-123"
}</code></pre>
                            </div>
                        </div>

                        <div class="highlight">
                            <p><i class="fas fa-code" style="color: var(--accent-primary); margin-right: 0.5rem;"></i> Полные примеры использования API доступны в разделе <a href="/p2p/docs/examples.html">"Примеры использования"</a>.</p>
                        </div>

                        <div class="nav-links">
                            <a href="/p2p/docs/examples.html"><i class="fas fa-arrow-left"></i> Примеры использования</a>
                            <a href="/p2p/docs/deployment.html"><i class="fas fa-server"></i> Развертывание <i class="fas fa-arrow-right"></i></a>
                        </div>
                    </div>
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
