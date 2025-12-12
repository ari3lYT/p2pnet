<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Развертывание - P2PNet</title>
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

        .deployment-option {
            background: var(--bg-tertiary);
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            margin: 2rem 0;
            position: relative;
            overflow: hidden;
        }

        .deployment-option::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: var(--gradient-primary);
        }

        .deployment-header {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
        }

        .deployment-icon {
            font-size: 2rem;
            margin-right: 1rem;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .deployment-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        .deployment-description {
            color: var(--text-secondary);
            margin-bottom: 1.5rem;
            line-height: 1.6;
        }

        .deployment-steps {
            counter-reset: step-counter;
        }

        .deployment-step {
            counter-increment: step-counter;
            margin-bottom: 1rem;
            padding-left: 2rem;
            position: relative;
        }

        .deployment-step::before {
            content: counter(step-counter);
            position: absolute;
            left: 0;
            top: 0;
            width: 1.5rem;
            height: 1.5rem;
            background: var(--gradient-primary);
            color: var(--bg-primary);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 0.9rem;
        }

        .config-example {
            background: var(--bg-secondary);
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            margin: 1rem 0;
        }

        .config-example h4 {
            color: var(--accent-primary);
            margin-bottom: 1rem;
            font-size: 1rem;
        }

        .config-example pre {
            background: var(--bg-tertiary);
            padding: 1rem;
            border-radius: 4px;
            margin: 0;
            font-size: 0.9rem;
        }

        .requirements-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }

        .requirements-table th,
        .requirements-table td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }

        .requirements-table th {
            background: var(--bg-secondary);
            color: var(--text-primary);
            font-weight: 600;
        }

        .requirements-table td {
            color: var(--text-secondary);
        }

        .requirements-table code {
            background: var(--bg-tertiary);
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            color: var(--accent-primary);
            font-family: 'Monaco', 'Menlo', monospace;
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
            
            .deployment-option {
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
                <h1>Развертывание P2PNet</h1>
                <p class="subtitle">Инструкции по установке и настройке узлов сети для различных сценариев использования</p>
            </section>

            <div class="content">
                <h2>Введение</h2>
                <p>P2PNet может быть развернут в различных конфигурациях в зависимости от ваших потребностей. Это руководство охватывает основные сценарии развертывания от локальной разработки до промышленного использования.</p>

                <div class="highlight">
                    <p><i class="fas fa-info-circle" style="color: var(--accent-primary); margin-right: 0.5rem;"></i> Перед началом развертывания убедитесь, что ваша система соответствует требованиям и установлены все необходимые зависимости.</p>
                </div>

                <h2>Системные требования</h2>

                <table class="requirements-table">
                    <thead>
                        <tr>
                            <th>Компонент</th>
                            <th>Минимальные требования</th>
                            <th>Рекомендуемые требования</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Операционная система</strong></td>
                            <td>Linux 18.04+, macOS 10.14+, Windows 10+</td>
                            <td>Linux 20.04+, macOS 11+</td>
                        </tr>
                        <tr>
                            <td><strong>Python</strong></td>
                            <td>3.8+</td>
                            <td>3.9+</td>
                        </tr>
                        <tr>
                            <td><strong>CPU</strong></td>
                            <td>2 ядра</td>
                            <td>4+ ядер</td>
                        </tr>
                        <tr>
                            <td><strong>Оперативная память</strong></td>
                            <td>4 GB</td>
                            <td>8+ GB</td>
                        </tr>
                        <tr>
                            <td><strong>Диск</strong></td>
                            <td>10 GB</td>
                            <td>50+ GB SSD</td>
                        </tr>
                        <tr>
                            <td><strong>Интернет</strong></td>
                            <td>10 Мбит/с</td>
                            <td>100+ Мбит/с</td>
                        </tr>
                    </tbody>
                </table>

                <h2>Типы развертывания</h2>

                <div class="deployment-option">
                    <div class="deployment-header">
                        <div class="deployment-icon">💻</div>
                        <div class="deployment-title">Локальная разработка</div>
                    </div>
                    <div class="deployment-description">
                        Идеально для тестирования, разработки и изучения работы P2PNet на локальной машине.
                    </div>
                    
                    <div class="deployment-steps">
                        <div class="deployment-step">
                            <h4>Клонирование репозитория</h4>
                            <pre><code>git clone https://github.com/ari3lYT/p2pnet.git
cd p2pnet</code></pre>
                        </div>
                        
                        <div class="deployment-step">
                            <h4>Создание виртуального окружения</h4>
                            <pre><code>python -m venv p2pnet-env
source p2pnet-env/bin/activate  # Linux/macOS
p2pnet-env\Scripts\activate     # Windows</code></pre>
                        </div>
                        
                        <div class="deployment-step">
                            <h4>Установка зависимостей</h4>
                            <pre><code>pip install -r requirements.txt</code></pre>
                        </div>
                        
                        <div class="deployment-step">
                            <h4>Настройка конфигурации</h4>
                            <div class="config-example">
                                <h4>config/local.json</h4>
                                <pre><code>{
  "node_id": "local-dev-node",
  "port": 8000,
  "max_cpu": 2,
  "max_memory": "4GB",
  "storage_path": "./data",
  "log_level": "DEBUG",
  "network_mode": "development",
  "bootstrap_nodes": []
}</code></pre>
                            </div>
                        </div>
                        
                        <div class="deployment-step">
                            <h4>Запуск узла</h4>
                            <pre><code>python src/main.py --config config/local.json</code></pre>
                        </div>
                    </div>
                </div>

                <div class="deployment-option">
                    <div class="deployment-header">
                        <div class="deployment-icon">🏢</div>
                        <div class="deployment-title">Корпоративная сеть</div>
                    </div>
                    <div class="deployment-description">
                        Развертывание P2PNet в корпоративной среде для использования внутри организации.
                    </div>
                    
                    <div class="deployment-steps">
                        <div class="deployment-step">
                            <h4>Подготовка инфраструктуры</h4>
                            <p>Убедитесь, что все серверы имеют доступ друг к другу и имеют статические IP-адреса.</p>
                        </div>
                        
                        <div class="deployment-step">
                            <h4>Установка на серверы</h4>
                            <pre><code># На каждом сервере
sudo apt update
sudo apt install python3 python3-pip git
git clone https://github.com/ari3lYT/p2pnet.git
cd p2pnet
python3 -m venv p2pnet-env
source p2pnet-env/bin/activate
pip install -r requirements.txt</code></pre>
                        </div>
                        
                        <div class="deployment-step">
                            <h4>Настройка конфигурации</h4>
                            <div class="config-example">
                                <h4>config/enterprise.json</h4>
                                <pre><code>{
  "node_id": "enterprise-node-01",
  "port": 8000,
  "max_cpu": 8,
  "max_memory": "16GB",
  "storage_path": "/data/p2pnet",
  "log_level": "INFO",
  "network_mode": "enterprise",
  "bootstrap_nodes": [
    "192.168.1.10:8000",
    "192.168.1.11:8000",
    "192.168.1.12:8000"
  ],
  "security": {
    "enable_ssl": true,
    "ssl_cert_path": "/etc/ssl/certs/p2pnet.crt",
    "ssl_key_path": "/etc/ssl/private/p2pnet.key"
  },
  "monitoring": {
    "enable_metrics": true,
    "metrics_port": 9090
  }
}</code></pre>
                            </div>
                        </div>
                        
                        <div class="deployment-step">
                            <h4>Создание systemd службы</h4>
                            <pre><code>sudo tee /etc/systemd/system/p2pnet.service > /dev/null <<EOF
[Unit]
Description=P2PNet Node
After=network.target

[Service]
Type=simple
User=p2pnet
WorkingDirectory=/opt/p2pnet
Environment=PATH=/opt/p2pnet/p2pnet-env/bin
ExecStart=/opt/p2pnet/p2pnet-env/bin/python src/main.py --config config/enterprise.json
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable p2pnet
sudo systemctl start p2pnet</code></pre>
                        </div>
                    </div>
                </div>

                <div class="deployment-option">
                    <div class="deployment-header">
                        <div class="deployment-icon">🌐</div>
                        <div class="deployment-title">Публичная сеть</div>
                    </div>
                    <div class="deployment-description">
                        Развертывание узлов в публичном доступе для создания глобальной децентрализованной сети.
                    </div>
                    
                    <div class="deployment-steps">
                        <div class="deployment-step">
                            <h4>Требования к инфраструктуре</h4>
                            <ul>
                                <li>Публичный IP-адрес</li>
                                <li>Открытые порты: 8000 (TCP/UDP)</li>
                                <li>Стабильное интернет-соединение</li>
                                <li>DNS-имя для узла</li>
                            </ul>
                        </div>
                        
                        <div class="deployment-step">
                            <h4>Настройка брандмауэра</h4>
                            <pre><code># Для Ubuntu/Debian
sudo ufw allow 8000/tcp
sudo ufw allow 8000/udp
sudo ufw enable

# Для CentOS/RHEL
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --permanent --add-port=8000/udp
sudo firewall-cmd --reload</code></pre>
                        </div>
                        
                        <div class="deployment-step">
                            <h4>Настройка конфигурации</h4>
                            <div class="config-example">
                                <h4>config/public.json</h4>
                                <pre><code>{
  "node_id": "public-node-001",
  "port": 8000,
  "max_cpu": 16,
  "max_memory": "32GB",
  "storage_path": "/data/p2pnet",
  "log_level": "INFO",
  "network_mode": "public",
  "bootstrap_nodes": [
    "node1.p2pnet.network:8000",
    "node2.p2pnet.network:8000"
  ],
  "security": {
    "enable_ssl": true,
    "ssl_cert_path": "/etc/letsencrypt/live/your-node.p2pnet.network/fullchain.pem",
    "ssl_key_path": "/etc/letsencrypt/live/your-node.p2pnet.network/privkey.pem"
  },
  "monitoring": {
    "enable_metrics": true,
    "metrics_port": 9090,
    "enable_alerts": true
  },
  "payments": {
    "enable_payments": true,
    "wallet_address": "0xYourEthereumAddress"
  }
}</code></pre>
                            </div>
                        </div>
                        
                        <div class="deployment-step">
                            <h4>Настройка Nginx (опционально)</h4>
                            <pre><code>server {
    listen 80;
    server_name your-node.p2pnet.network;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /metrics {
        proxy_pass http://localhost:9090;
        proxy_set_header Host $host;
    }
}</code></pre>
                        </div>
                    </div>
                </div>

                <div class="deployment-option">
                    <div class="deployment-header">
                        <div class="deployment-icon">☸️</div>
                        <div class="deployment-title">Docker/Kubernetes</div>
                    </div>
                    <div class="deployment-description">
                        Контейнеризированное развертывание P2PNet с использованием Docker и Kubernetes.
                    </div>
                    
                    <div class="deployment-steps">
                        <div class="deployment-step">
                            <h4>Создание Dockerfile</h4>
                            <pre><code>FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

EXPOSE 8000 9090

CMD ["python", "src/main.py", "--config", "config/docker.json"]</code></pre>
                        </div>
                        
                        <div class="deployment-step">
                            <h4>Сборка образа</h4>
                            <pre><code>docker build -t p2pnet-node:latest .</code></pre>
                        </div>
                        
                        <div class="deployment-step">
                            <h4>Запуск контейнера</h4>
                            <pre><code>docker run -d \
  --name p2pnet-node \
  -p 8000:8000 \
  -p 9090:9090 \
  -v /data/p2pnet:/data/p2pnet \
  p2pnet-node:latest</code></pre>
                        </div>
                        
                        <div class="deployment-step">
                            <h4>Deployment YAML для Kubernetes</h4>
                            <pre><code>apiVersion: apps/v1
kind: Deployment
metadata:
  name: p2pnet-node
spec:
  replicas: 3
  selector:
    matchLabels:
      app: p2pnet
  template:
    metadata:
      labels:
        app: p2pnet
    spec:
      containers:
      - name: p2pnet
        image: p2pnet-node:latest
        ports:
        - containerPort: 8000
        - containerPort: 9090
        volumeMounts:
        - name: data
          mountPath: /data/p2pnet
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: p2pnet-data</code></pre>
                        </div>
                    </div>
                </div>

                <h2>Оптимизация производительности</h2>

                <div class="deployment-option">
                    <div class="deployment-header">
                        <div class="deployment-icon">⚡</div>
                        <div class="deployment-title">Настройка для максимальной производительности</div>
                    </div>
                    <div class="deployment-description">
                        Рекомендации по оптимизации производительности узлов P2PNet.
                    </div>
                    
                    <h4>Оптимизация системы</h4>
                    <ul>
                        <li>Используйте SSD для хранения данных</li>
                        <li>Выделите достаточное количество CPU ядер</li>
                        <li>Настройте swap-память для обработки пиковых нагрузок</li>
                        <li>Оптимизируйте сетевые настройки</li>
                    </ul>
                    
                    <h4>Настройка ядра Linux</h4>
                    <pre><code># Увеличение лимитов файловых дескрипторов
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# Настройка сетевых параметров
sudo sysctl -w net.core.somaxconn=65535
sudo sysctl -w net.ipv4.tcp_max_syn_backlog=65535
sudo sysctl -w net.core.netdev_max_backlog=65535

# Применение настроек
sudo sysctl -p</code></pre>
                    
                    <h4>Настройка P2PNet</h4>
                    <div class="config-example">
                        <h4>config/optimized.json</h4>
                        <pre><code>{
  "node_id": "optimized-node",
  "port": 8000,
  "max_cpu": 32,
  "max_memory": "64GB",
  "storage_path": "/data/p2pnet",
  "log_level": "INFO",
  "performance": {
    "worker_threads": 16,
    "connection_pool_size": 100,
    "task_queue_size": 1000,
    "cache_size": "1GB"
  },
  "network": {
    "max_connections": 1000,
    "timeout": 30,
    "retry_attempts": 3
  },
  "monitoring": {
    "enable_metrics": true,
    "metrics_interval": 10,
    "enable_profiling": true
  }
}</code></pre>
                    </div>
                </div>

                <h2>Мониторинг и логирование</h2>

                <div class="deployment-option">
                    <div class="deployment-header">
                        <div class="deployment-icon">📊</div>
                        <div class="deployment-title">Настройка мониторинга</div>
                    </div>
                    <div class="deployment-description">
                        Настройка систем мониторинга для отслеживания состояния узлов P2PNet.
                    </div>
                    
                    <h4>Использование Prometheus + Grafana</h4>
                    <pre><code># docker-compose.yml для мониторинга
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    depends_on:
      - prometheus</code></pre>
                    
                    <h4>Пример конфигурации Prometheus</h4>
                    <pre><code>global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'p2pnet'
    static_configs:
      - targets: ['localhost:9090']
    metrics_path: '/metrics'</code></pre>
                </div>

                <div class="highlight">
                    <p><i class="fas fa-check-circle" style="color: var(--accent-primary); margin-right: 0.5rem;"></i> После развертывания узла рекомендуется регулярно обновлять P2PNet до последних версий и следовать рекомендациям по безопасности.</p>
                </div>

                <div class="nav-links">
                    <a href="/p2p/docs/api-reference.html"><i class="fas fa-arrow-left"></i> API Ссылка</a>
                    <a href="/p2p/docs/"><i class="fas fa-book"></i> Документация <i class="fas fa-arrow-right"></i></a>
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