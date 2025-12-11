# 🚀 Развертывание и эксплуатация

## 📋 Содержание

- [Обзор развертывания](#обзор-развертывания)
- [Требования системы](#требования-системы)
- [Установка и настройка](#установка-и-настройка)
- [Конфигурация](#конфигурация)
- [Развертывание в разных средах](#развертывание-в-разных-средах)
- [Мониторинг и логирование](#мониторинг-и-логирование)
- [Обновление и обслуживание](#обновление-и-обслуживание)
- [Резервное копирование](#резервное-копирование)
- [Безопасность](#безопасность)
- [Производительность](#производительность)
- [Отладка](#отладка)

---

## 🎯 Обзор развертывания

Децентрализованная P2P вычислительная сеть может быть развернута в различных конфигурациях - от локальной разработки до промышленного масштаба. Эта документация охватывает все аспекты развертывания и эксплуатации.

### Варианты развертывания

1. **Локальная разработка** - для разработки и тестирования
2. **Развертывание на одном сервере** - для небольших сетей
3. **Кластерное развертывание** - для средних и крупных сетей
4. **Облачное развертывание** - для гибкости и масштабирования
5. **Гибридное развертывание** - комбинирование различных подходов

### Архитектура развертывания

```
┌─────────────────────────────────────────────────────────────┐
│                    Среда развертывания                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Локальная │  │   Облачная  │  │   Гибридная │          │
│  │   среда     │  │   среда     │  │   среда     │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
├─────────────────────────────────────────────────────────────┤
│                  Сеть вычислительных узлов                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Узел 1    │  │   Узел 2    │  │   Узел 3    │  ...      │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
├─────────────────────────────────────────────────────────────┤
│                   Инфраструктура поддержки                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Мониторинг│  │   Логирование│  │   Резервное │          │
│  │   и Аналитика│ │   и Отладка │  │   копирование│          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Требования системы

### Аппаратные требования

#### Минимальные требования

```yaml
# Для одного узла
hardware:
  cpu: "2 ядра"
  ram: "4 GB"
  storage: "50 GB SSD"
  network: "100 Mbps"
  gpu: "Не требуется"
  
# Для seed-узла
hardware_seed:
  cpu: "4 ядра"
  ram: "8 GB"
  storage: "100 GB SSD"
  network: "1 Gbps"
  gpu: "Не требуется"
  
# Для узла с GPU
hardware_gpu:
  cpu: "8 ядер"
  ram: "16 GB"
  storage: "200 GB SSD"
  network: "1 Gbps"
  gpu: "1 GPU с 8GB VRAM"
```

#### Рекомендуемые требования

```yaml
# Для производительного узла
hardware_recommended:
  cpu: "8+ ядер"
  ram: "32+ GB"
  storage: "500+ GB NVMe SSD"
  network: "10+ Gbps"
  gpu: "2+ GPU с 16GB VRAM"
  
# Для кластера
hardware_cluster:
  nodes: "10+ узлов"
  network: "25+ Gbps InfiniBand"
  storage: "Distributed storage"
  monitoring: "Prometheus + Grafana"
  load_balancer: "HAProxy"
```

### Программные требования

```yaml
# Операционная система
os:
  - "Ubuntu 20.04 LTS"
  - "Ubuntu 22.04 LTS"
  - "CentOS 8"
  - "RHEL 8"
  - "Debian 11"
  - "Windows Server 2019+"

# Python и зависимости
python:
  version: "3.9+"
  packages:
    - "asyncio"
    - "aiohttp"
    - "websockets"
    - "numpy"
    - "pandas"
    - "scikit-learn"
    - "torch"
    - "tensorflow"
    - "docker"
    - "kubernetes"

# Системные утилиты
system:
  - "git"
  - "curl"
  - "wget"
  - "htop"
  - "tmux"
  - "screen"
  - "jq"
  - "yq"
  - "docker-compose"
  
# Сеть
network:
  - "Nginx"
  - "HAProxy"
  - "Keepalived"
  - "WireGuard"
  - "OpenVPN"
  
# Мониторинг
monitoring:
  - "Prometheus"
  - "Grafana"
  - "Alertmanager"
  - "Node Exporter"
  - "Blackbox Exporter"
  
# Логирование
logging:
  - "ELK Stack (Elasticsearch, Logstash, Kibana)"
  - "Loki"
  - "Fluentd"
  - "Filebeat"
```

### Сетевые требования

```yaml
# Базовые сетевые требования
network:
  # Минимальные требования
  min_bandwidth: "100 Mbps"
  min_latency: "< 100ms"
  min_jitter: "< 20ms"
  packet_loss: "< 1%"
  
  # Рекомендуемые требования
  recommended_bandwidth: "1+ Gbps"
  recommended_latency: "< 50ms"
  recommended_jitter: "< 10ms"
  packet_loss: "< 0.1%"
  
  # Порты
  ports:
    - "5557:5557"     # Основной порт P2P
    - "5558:5558"     # Альтернативный порт
    - "8080:8080"     # HTTP API
    - "8443:8443"     # HTTPS API
    - "9090:9090"     # Prometheus
    - "3000:3000"     # Grafana
    
  # Протоколы
  protocols:
    - "TCP/UDP"       # P2P коммуникация
    - "HTTP/HTTPS"    # REST API
    - "WebSocket"     # Real-time updates
    - "gRPC"          # High-performance RPC
```

---

## 🛠️ Установка и настройка

### Установка из исходного кода

#### Шаг 1: Клонирование репозитория

```bash
# Клонирование репозитория
git clone https://github.com/your-org/compute-network.git
cd compute-network

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

#### Шаг 2: Установка системных зависимостей

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y \
    python3-dev \
    python3-pip \
    build-essential \
    git \
    curl \
    wget \
    nginx \
    supervisor

# CentOS/RHEL
sudo yum update -y
sudo yum install -y \
    python3-devel \
    python3-pip \
    gcc \
    git \
    curl \
    wget \
    nginx \
    supervisor

# Windows (PowerShell)
choco install python git nginx supervisor
```

#### Шаг 3: Настройка окружения

```bash
# Создание директорий
mkdir -p /opt/compute-network/{logs,data,config,backups}

# Копирование конфигурации
cp config/network_config.json /opt/compute-network/config/
cp config/supervisor.conf /etc/supervisor/conf.d/compute-network.conf

# Настройка прав доступа
sudo chown -R $USER:$USER /opt/compute-network
sudo chmod -R 755 /opt/compute-network
```

#### Шаг 4: Установка Python зависимостей

```bash
# Активация виртуального окружения
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Установка в development mode
pip install -e .
```

### Установка с помощью Docker

#### Шаг 1: Установка Docker

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# CentOS/RHEL
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER
```

#### Шаг 2: Создание Dockerfile

```dockerfile
# Dockerfile
FROM python:3.9-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Копирование кода
WORKDIR /app
COPY src/ ./src/
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование конфигурации
COPY config/ ./config/

# Создание пользователя
RUN useradd -m -u 1000 compute
USER compute

# Открытие портов
EXPOSE 5557 5558 8080 8443

# Запуск приложения
CMD ["python", "-m", "main"]
```

#### Шаг 3: Сборка Docker образа

```bash
# Сборка образа
docker build -t compute-network:latest .

# Запуск контейнера
docker run -d \
    --name compute-network \
    -p 5557:5557 \
    -p 5558:5558 \
    -p 8080:8080 \
    -v $(pwd)/config:/app/config \
    -v $(pwd)/logs:/app/logs \
    compute-network:latest
```

#### Шаг 4: Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  compute-network:
    build: .
    ports:
      - "5557:5557"
      - "5558:5558"
      - "8080:8080"
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
      - ./data:/app/data
    environment:
      - NODE_TYPE=public
      - SEED_NODES=seed1:5557,seed2:5557
    restart: unless-stopped
    
  seed-node:
    build: .
    ports:
      - "5557:5557"
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
    environment:
      - NODE_TYPE=seed
    restart: unless-stopped
    command: ["python", "-m", "main", "--seed-mode"]
```

```bash
# Запcompose
docker-compose up -d
```

---

## ⚙️ Конфигурация

### Конфигурационный файл

```json
// config/network_config.json
{
    "node": {
        "node_id": "node-001",
        "host": "0.0.0.0",
        "port": 5557,
        "node_type": "public",
        "capabilities": {
            "cpu_score": 8.0,
            "ram_gb": 16.0,
            "disk_gb": 500.0,
            "gpu_score": 2.0,
            "max_concurrent_tasks": 20
        }
    },
    "network": {
        "seed_nodes": [
            "seed1.example.com:5557",
            "seed2.example.com:5557"
        ],
        "discovery": {
            "method": "udp_broadcast",
            "port": 5558,
            "interval": 30
        },
        "routing": {
            "algorithm": "distance_vector",
            "update_interval": 60
        }
    },
    "security": {
        "encryption": {
            "enabled": true,
            "algorithm": "TLS_1.3",
            "certificate_path": "certs/node.crt",
            "private_key_path": "certs/node.key"
        },
        "authentication": {
            "method": "certificate",
            "require_seed_signature": true
        },
        "sandbox": {
            "type": "process_isolation",
            "resource_limits": {
                "cpu_time_seconds": 300,
                "memory_bytes": 1073741824,
                "file_size_bytes": 536870912
            }
        }
    },
    "pricing": {
        "base_prices": {
            "cpu": 0.01,
            "gpu": 0.05,
            "ram": 0.02,
            "disk": 0.005
        },
        "multipliers": {
            "urgency": {
                "low": 0.8,
                "normal": 1.0,
                "high": 1.5,
                "critical": 2.0
            }
        }
    },
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "logs/network.log",
        "max_size": "10MB",
        "backup_count": 5
    },
    "monitoring": {
        "enabled": true,
        "metrics_port": 8080,
        "health_check_interval": 30
    }
}
```

### Переменные окружения

```bash
# .env файл
NODE_ID=node-001
NODE_HOST=0.0.0.0
NODE_PORT=5557
NODE_TYPE=public
SEED_NODES=seed1:5557,seed2:5557
CONFIG_PATH=/opt/compute-network/config/network_config.json
LOG_LEVEL=INFO
LOG_FILE=/opt/compute-network/logs/network.log
METRICS_PORT=8080
HEALTH_CHECK_INTERVAL=30
```

### Конфигурация Supervisor

```ini
# /etc/supervisor/conf.d/compute-network.conf
[program:compute-network]
command=/opt/compute-network/venv/bin/python -m main
directory=/opt/compute-network
user=compute
autostart=true
autorestart=true
startsecs=10
startretries=5
stopwaitsecs=3600
stopasgroup=true
killasgroup=true
stdout_logfile=/opt/compute-network/logs/supervisor.log
stderr_logfile=/opt/compute-network/logs/supervisor.err.log
environment=NODE_ID="node-001",NODE_HOST="0.0.0.0",NODE_PORT="5557"
```

### Конфигурация Nginx

```nginx
# /etc/nginx/sites-available/compute-network
server {
    listen 80;
    server_name compute-network.local;
    
    # HTTP -> HTTPS редирект
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name compute-network.local;
    
    # SSL сертификаты
    ssl_certificate /etc/ssl/certs/compute-network.crt;
    ssl_certificate_key /etc/ssl/private/compute-network.key;
    
    # Безопасность
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # API прокси
    location /api/ {
        proxy_pass http://localhost:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket поддержка
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # Статические файлы
    location / {
        root /opt/compute-network/web;
        try_files $uri $uri/ =404;
    }
    
    # Метрики Prometheus
    location /metrics {
        proxy_pass http://localhost:8080/metrics;
        proxy_set_header Host $host;
    }
    
    # Лимиты запросов
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    
    location /api/ {
        limit_req zone=api burst=20 nodelay;
    }
}
```

---

## 🌐 Развертывание в разных средах

### Локальная разработка

```bash
# Запуск в режиме разработки
export NODE_TYPE=client
export SEED_NODES=localhost:5557
export LOG_LEVEL=DEBUG
export DEBUG=True

python -m main --dev-mode
```

### Развертывание на одном сервере

```bash
# Создание systemd сервиса
sudo tee /etc/systemd/system/compute-network.service << EOF
[Unit]
Description=Compute Network Service
After=network.target

[Service]
Type=simple
User=compute
WorkingDirectory=/opt/compute-network
Environment=NODE_TYPE=public
Environment=SEED_NODES=seed1.example.com:5557
ExecStart=/opt/compute-network/venv/bin/python -m main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Запуск сервиса
sudo systemctl daemon-reload
sudo systemctl enable compute-network
sudo systemctl start compute-network
```

### Кластерное развертывание

#### Kubernetes

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: compute-network
spec:
  replicas: 3
  selector:
    matchLabels:
      app: compute-network
  template:
    metadata:
      labels:
        app: compute-network
    spec:
      containers:
      - name: compute-network
        image: compute-network:latest
        ports:
        - containerPort: 5557
        - containerPort: 8080
        env:
        - name: NODE_TYPE
          value: "public"
        - name: SEED_NODES
          value: "seed-service:5557"
        resources:
          requests:
            cpu: "1"
            memory: "2Gi"
          limits:
            cpu: "2"
            memory: "4Gi"
        volumeMounts:
        - name: config
          mountPath: /app/config
        - name: data
          mountPath: /app/data
        - name: logs
          mountPath: /app/logs
      volumes:
      - name: config
        configMap:
          name: compute-network-config
      - name: data
        persistentVolumeClaim:
          claimName: compute-network-data
      - name: logs
        persistentVolumeClaim:
          claimName: compute-network-logs
```

```yaml
# k8s-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: compute-network-service
spec:
  selector:
    app: compute-network
  ports:
  - port: 5557
    targetPort: 5557
    name: p2p
  - port: 8080
    targetPort: 8080
    name: api
  type: LoadBalancer
```

#### Docker Swarm

```yaml
# docker-stack.yml
version: '3.8'

services:
  compute-network:
    image: compute-network:latest
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
    ports:
      - "5557:5557"
      - "8080:8080"
    environment:
      - NODE_TYPE=public
      - SEED_NODES=seed1:5557,seed2:5557
    volumes:
      - ./config:/app/config
      - ./data:/app/data
      - ./logs:/app/logs
    networks:
      - compute-network

  seed-node:
    image: compute-network:latest
    deploy:
      replicas: 2
      placement:
        constraints: [node.role == manager]
    ports:
      - "5557:5557"
    environment:
      - NODE_TYPE=seed
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
    networks:
      - compute-network

networks:
  compute-network:
    driver: overlay
```

### Облачное развертывание

#### AWS

```bash
# AWS CloudFormation шаблон
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Compute Network Deployment'

Parameters:
  InstanceType:
    Type: String
    Default: t3.large
    AllowedValues:
      - t3.large
      - t3.xlarge
      - t3.2xlarge
    Description: 'EC2 Instance Type'

  VpcCIDR:
    Type: String
    Default: '10.0.0.0/16'
    Description: 'VPC CIDR'

Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Ref VpcCIDR
      EnableDnsSupport: true
      EnableDnsHostnames: true

  Subnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: '10.0.1.0/24'
      MapPublicIpOnLaunch: true

  SecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      VpcId: !Ref VPC
      GroupDescription: 'Compute Network Security Group'
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 5557
          ToPort: 5557
          CidrIp: '0.0.0.0/0'
        - IpProtocol: tcp
          FromPort: 8080
          ToPort: 8080
          CidrIp: '0.0.0.0/0'

  Instance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: !Ref InstanceType
      SubnetId: !Ref Subnet
      SecurityGroupIds:
        - !Ref SecurityGroup
      UserData:
        Fn::Base64: !Sub |
          #!/bin/bash -xe
          apt-get update -y
          apt-get install -y python3 python3-pip docker.io
          pip3 install docker-compose
          docker swarm init
          docker stack deploy -c docker-stack.yml compute-network
```

#### Google Cloud Platform

```bash
# Terraform конфигурация
resource "google_compute_instance" "compute_network" {
  name         = "compute-network-node"
  machine_type = "e2-medium"
  zone         = "us-central1-a"
  
  boot_disk {
    initialize_params {
      image = "ubuntu-2004-lts"
    }
  }
  
  network_interface {
    network = "default"
    access_config {}
  }
  
  metadata = {
    ssh-keys = "compute:${file("~/.ssh/id_rsa.pub")}"
  }
  
  tags = ["compute-network"]
}

resource "google_compute_firewall" "compute_network" {
  name    = "compute-network-firewall"
  network = "default"
  
  allow {
    protocol = "tcp"
    ports    = ["5557", "8080"]
  }
  
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["compute-network"]
}
```

---

## 📊 Мониторинг и логирование

### Prometheus мониторинг

#### Конфигурация Prometheus

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "compute-network.rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets: ["localhost:9093"]

scrape_configs:
  - job_name: 'compute-network'
    static_configs:
      - targets: ['localhost:8080']
    scrape_interval: 5s
    metrics_path: '/metrics'
    
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['localhost:9100']
```

#### Метрики Compute Network

```python
# src/monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

class NetworkMetrics:
    def __init__(self):
        # Счетчики
        self.tasks_total = Counter('tasks_total', 'Total tasks created', ['task_type', 'status'])
        self.tasks_completed = Counter('tasks_completed', 'Completed tasks', ['task_type'])
        self.tasks_failed = Counter('tasks_failed', 'Failed tasks', ['task_type', 'error_type'])
        
        # Гистограммы
        self.task_duration = Histogram('task_duration_seconds', 'Task execution time', ['task_type'])
        self.network_latency = Histogram('network_latency_ms', 'Network latency')
        
        # Гейжи
        self.active_nodes = Gauge('active_nodes', 'Number of active nodes')
        self.active_tasks = Gauge('active_tasks', 'Number of active tasks')
        self.cpu_usage = Gauge('cpu_usage_percent', 'CPU usage percentage')
        self.ram_usage = Gauge('ram_usage_percent', 'RAM usage percentage')
        self.network_bandwidth = Gauge('network_bandwidth_mbps', 'Network bandwidth usage')
        
        # Запуск HTTP сервера для метрик
        start_http_server(8080)

# Регистрация метрик
metrics = NetworkMetrics()

# Использование метрик
def track_task_execution(task_type, execution_time, success):
    with metrics.task_duration.labels(task_type=task_type).time():
        if success:
            metrics.tasks_completed.labels(task_type=task_type).inc()
        else:
            metrics.tasks_failed.labels(task_type=task_type, error_type="unknown").inc()
```

#### Правила оповещений

```yaml
# compute-network.rules.yml
groups:
  - name: compute-network
    rules:
      - alert: HighTaskFailureRate
        expr: rate(tasks_failed[5m]) / rate(tasks_total[5m]) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High task failure rate"
          description: "Task failure rate is {{ $value }} (threshold 0.1)"
          
      - alert: LowActiveNodes
        expr: active_nodes < 3
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Low number of active nodes"
          description: "Only {{ $value }} active nodes (threshold 3)"
          
      - alert: HighCPUUsage
        expr: cpu_usage_percent > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage"
          description: "CPU usage is {{ $value }}%"
          
      - alert: HighRAMUsage
        expr: ram_usage_percent > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High RAM usage"
          description: "RAM usage is {{ $value }}%"
```

### Grafana дашборды

#### Дашборд сети

```json
{
  "dashboard": {
    "title": "Compute Network Overview",
    "panels": [
      {
        "title": "Active Nodes",
        "type": "stat",
        "targets": [
          {
            "expr": "active_nodes",
            "legendFormat": "Nodes"
          }
        ]
      },
      {
        "title": "Task Execution Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(tasks_total[5m])",
            "legendFormat": "Total"
          },
          {
            "expr": "rate(tasks_completed[5m])",
            "legendFormat": "Completed"
          },
          {
            "expr": "rate(tasks_failed[5m])",
            "legendFormat": "Failed"
          }
        ]
      },
      {
        "title": "Task Duration by Type",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(task_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.50, rate(task_duration_seconds_bucket[5m]))",
            "legendFormat": "50th percentile"
          }
        ]
      },
      {
        "title": "Resource Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "cpu_usage_percent",
            "legendFormat": "CPU"
          },
          {
            "expr": "ram_usage_percent",
            "legendFormat": "RAM"
          }
        ]
      }
    ]
  }
}
```

### Логирование

#### Конфигурация логирования

```python
# src/logging/config.py
import logging
import logging.handlers
import os
from datetime import datetime

def setup_logging(config):
    """Настройка системы логирования"""
    
    # Создание директорий для логов
    log_dir = config.get('logging', {}).get('log_dir', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Форматирование логов
    log_format = config.get('logging', {}).get('format', 
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Уровень логирования
    log_level = getattr(logging, config.get('logging', {}).get('level', 'INFO').upper())
    
    # Создание логгера
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Файловый обработчик с ротацией
    log_file = os.path.join(log_dir, f'compute_network_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)
    
    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(console_handler)
    
    # Логирование ошибок в отдельный файл
    error_log_file = os.path.join(log_dir, 'errors.log')
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=10*1024*1024,
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(error_handler)
    
    return logger
```

#### Структура логов

```
logs/
├── compute_network_20251208.log    # Основной лог файл
├── compute_network_20251209.log    # Основной лог файл (следующий день)
├── errors.log                      # Ошибки и исключения
├── audit.log                       # Аудитные события
├── access.log                      # Логи доступа
└── metrics.log                     # Метрики и статистика
```

---

## 🔄 Обновление и обслуживание

### Обновление системы

#### Обновление из исходного кода

```bash
# Обновление кода
cd /opt/compute-network
git pull origin main

# Обновление зависимостей
source venv/bin/activate
pip install -r requirements.txt
pip install -e .

# Перезапуск сервиса
sudo systemctl restart compute-network

# Проверка статуса
sudo systemctl status compute-network
```

#### Обновление Docker

```bash
# Остановка старого контейнера
docker stop compute-network
docker rm compute-network

# Сборка нового образа
docker build -t compute-network:latest .

# Запуск нового контейнера
docker run -d \
    --name compute-network \
    -p 5557:5557 \
    -p 8080:8080 \
    -v $(pwd)/config:/app/config \
    -v $(pwd)/logs:/app/logs \
    compute-network:latest
```

#### Обновление Kubernetes

```bash
# Обновление образа в деплойменте
kubectl set image deployment/compute-network compute-network=compute-network:latest

# Отслеживание обновления
kubectl rollout status deployment/compute-network

# Откат при необходимости
kubectl rollout undo deployment/compute-network
```

### Плановое обслуживание

#### Обновление зависимостей

```bash
# Проверка обновлений pip
pip list --outdated

# Обновление всех пакетов
pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U

# Обновление системы безопасности
apt-get update && apt-get upgrade -y
```

#### Очистка системы

```bash
# Очистка логов
find /opt/compute-network/logs -name "*.log" -mtime +30 -delete

# Очистка кэша
find /opt/compute-network -name "__pycache__" -type d -exec rm -rf {} +
find /opt/compute-network -name "*.pyc" -delete

# Очистка Docker
docker system prune -f

# Очистка Kubernetes
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}' | grep -Ev "^(kube|coredns)" | xargs -n 1 kubectl delete pod --namespace=default
```

### Резервное копирование

#### Скрипт резервного копирования

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/opt/compute-network/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="compute_network_backup_$DATE.tar.gz"

# Создание бэкапа
tar -czf "$BACKUP_DIR/$BACKUP_FILE" \
    /opt/compute-network/config \
    /opt/compute-network/data \
    /opt/compute-network/logs \
    /opt/compute-network/venv/lib/python*/site-packages

# Удаление старых бэкапов (оставляем последние 7)
find "$BACKUP_DIR" -name "compute_network_backup_*.tar.gz" -mtime +7 -delete

# Загрузка в облако (опционально)
# aws s3 cp "$BACKUP_DIR/$BACKUP_FILE" s3://compute-network-backups/

echo "Backup completed: $BACKUP_FILE"
```

#### Автоматизация бэкапов

```bash
# Добавление в crontab
0 2 * * * /opt/compute-network/scripts/backup.sh
```

---

## 🔒 Безопасность

### Конфигурация безопасности

#### SSL/TLS сертификаты

```bash
# Генерация самоподписанного сертификата
openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes

# Или использование Let's Encrypt
sudo apt-get install certbot
sudo certbot certonly --standalone -d compute-network.example.com

# Настройка Nginx с SSL
server {
    listen 443 ssl http2;
    server_name compute-network.example.com;
    
    ssl_certificate /etc/letsencrypt/live/compute-network.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/compute-network.example.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
}
```

#### Фаервол

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 5557/tcp
sudo ufw allow 8080/tcp
sudo ufw enable

# iptables
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 5557 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
sudo iptables -A INPUT -j DROP
```

#### SSH безопасность

```bash
# Отключение root SSH
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Запрет парольной аутентификации
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# Перезапуск SSH
sudo systemctl restart sshd
```

### Мониторинг безопасности

#### Логи безопасности

```python
# src/security/monitor.py
import logging
from datetime import datetime, timedelta

class SecurityMonitor:
    def __init__(self):
        self.logger = logging.getLogger('security')
        self.failed_logins = {}
        self.suspicious_ips = set()
        
    def log_failed_login(self, ip_address, username):
        """Логирование неудачных попыток входа"""
        
        if ip_address not in self.failed_logins:
            self.failed_logins[ip_address] = []
            
        self.failed_logins[ip_address].append({
            'timestamp': datetime.now(),
            'username': username
        })
        
        # Проверка на брутфорс
        recent_attempts = [
            attempt for attempt in self.failed_logins[ip_address]
            if attempt['timestamp'] > datetime.now() - timedelta(minutes=15)
        ]
        
        if len(recent_attempts) > 5:
            self.suspicious_ips.add(ip_address)
            self.logger.warning(f"Potential brute force attack from {ip_address}")
            
    def check_suspicious_activity(self, ip_address):
        """Проверка подозрительной активности"""
        
        if ip_address in self.suspicious_ips:
            self.logger.warning(f"Suspicious activity from {ip_address}")
            return True
            
        return False
```

#### Скрипт безопасности

```bash
#!/bin/bash
# security_check.sh

echo "Running security checks..."

# Проверка обновлений безопасности
echo "Checking for security updates..."
apt-get update && apt-get upgrade -y

# Проверка открытых портов
echo "Checking open ports..."
netstat -tuln | grep -E '5557|8080'

# Проверка логов на подозрительную активность
echo "Checking logs for suspicious activity..."
grep -i "failed\|error\|denied" /var/log/auth.log | tail -20

# Проверка дискового пространства
echo "Checking disk space..."
df -h

# Проверка использования памяти
echo "Checking memory usage..."
free -h

echo "Security checks completed."
```

---

## ⚡ Производительность

### Оптимизация производительности

#### Конфигурация ядра Linux

```bash
# Настройка параметров ядра
cat >> /etc/sysctl.conf << EOF
# Network optimization
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 4096 87380 134217728
net.ipv4.tcp_wmem = 4096 65536 134217728
net.core.netdev_max_backlog = 5000
net.ipv4.tcp_congestion_control = bbr

# File system optimization
vm.swappiness = 10
vm.vfs_cache_pressure = 50

# File descriptor limits
fs.file-max = 1000000
EOF

# Применение изменений
sysctl -p
```

#### Настройка Python

```python
# src/performance/config.py
import os
import multiprocessing

class PerformanceConfig:
    def __init__(self):
        # Оптимизация для многопроцессорных систем
        self.cpu_count = multiprocessing.cpu_count()
        self.max_workers = min(32, self.cpu_count * 4)
        
        # Оптимизация памяти
        self.memory_limit = os.environ.get('MEMORY_LIMIT', '4g')
        self.gc_threshold = 10000
        
        # Оптимизация сети
        self.buffer_size = 65536
        self.max_connections = 1000
        
        # Оптимизация базы данных
        self.db_pool_size = 20
        self.db_max_overflow = 30
        
        # Оптимизация кэша
        self.cache_size = 1000
        self.cache_ttl = 3600
```

#### Профилирование производительности

```python
# src/performance/profiler.py
import cProfile
import pstats
import io
from contextlib import redirect_stdout

class PerformanceProfiler:
    def __init__(self):
        self.profiler = cProfile.Profile()
        
    def start(self):
        """Начало профилирования"""
        self.profiler.enable()
        
    def stop(self, output_file='performance_stats.prof'):
        """Окончание профилирования"""
        self.profiler.disable()
        
        # Сохранение статистики
        stats = pstats.Stats(self.profiler)
        stats.sort_stats('cumulative')
        stats.dump_stats(output_file)
        
        # Вывод статистики в консоль
        stats.print_stats(10)
        
        return stats
```

### Нагрузочное тестирование

#### Скрипт нагрузочного тестирования

```python
# src/testing/load_test.py
import asyncio
import aiohttp
import time
import random
from typing import List, Dict

class LoadTester:
    def __init__(self, base_url: str, concurrent_users: int = 10):
        self.base_url = base_url
        self.concurrent_users = concurrent_users
        self.results = []
        
    async def test_endpoint(self, endpoint: str, method: str = 'GET', data: Dict = None):
        """Тестирование эндпоинта"""
        
        start_time = time.time()
        success = False
        error = None
        
        try:
            async with aiohttp.ClientSession() as session:
                if method == 'GET':
                    async with session.get(f"{self.base_url}{endpoint}") as response:
                        if response.status == 200:
                            success = True
                        else:
                            error = f"HTTP {response.status}"
                elif method == 'POST':
                    async with session.post(f"{self.base_url}{endpoint}", json=data) as response:
                        if response.status == 200:
                            success = True
                        else:
                            error = f"HTTP {response.status}"
                            
        except Exception as e:
            error = str(e)
            
        end_time = time.time()
        duration = end_time - start_time
        
        result = {
            'endpoint': endpoint,
            'method': method,
            'success': success,
            'duration': duration,
            'error': error,
            'timestamp': time.time()
        }
        
        self.results.append(result)
        return result
        
    async def run_concurrent_test(self, endpoints: List[str], duration: int = 60):
        """Запуск параллельного тестирования"""
        
        start_time = time.time()
        
        async def worker():
            while time.time() - start_time < duration:
                endpoint = random.choice(endpoints)
                await self.test_endpoint(endpoint)
                await asyncio.sleep(random.uniform(0.1, 1.0))
                
        tasks = [worker() for _ in range(self.concurrent_users)]
        await asyncio.gather(*tasks)
        
    def generate_report(self):
        """Генерация отчета о тестировании"""
        
        total_requests = len(self.results)
        successful_requests = sum(1 for r in self.results if r['success'])
        failed_requests = total_requests - successful_requests
        
        avg_duration = sum(r['duration'] for r in self.results) / total_requests
        success_rate = (successful_requests / total_requests) * 100
        
        report = {
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'failed_requests': failed_requests,
            'success_rate': success_rate,
            'average_duration': avg_duration,
            'requests_per_second': total_requests / (self.results[-1]['timestamp'] - self.results[0]['timestamp'])
        }
        
        return report
```

---

## 🐛 Отладка

### Инструменты отладки

#### Логирование отладочной информации

```python
# src/debug/logger.py
import logging
import sys
from datetime import datetime

class DebugLogger:
    def __init__(self, name: str = 'debug'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Форматирование
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Консольный вывод
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Файловый вывод
        file_handler = logging.FileHandler(f'debug_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
    def debug(self, message: str, **kwargs):
        """Отладочное сообщение"""
        self.logger.debug(message, **kwargs)
        
    def info(self, message: str, **kwargs):
        """Информационное сообщение"""
        self.logger.info(message, **kwargs)
        
    def warning(self, message: str, **kwargs):
        """Предупреждение"""
        self.logger.warning(message, **kwargs)
        
    def error(self, message: str, **kwargs):
        """Ошибка"""
        self.logger.error(message, **kwargs)
        
    def critical(self, message: str, **kwargs):
        """Критическая ошибка"""
        self.logger.critical(message, **kwargs)
```

#### Профилирование производительности

```python
# src/debug/profiler.py
import cProfile
import pstats
import time
from contextlib import contextmanager

@contextmanager
def profile_function(name: str):
    """Контекстный менеджер для профилирования функций"""
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    start_time = time.time()
    
    try:
        yield
    finally:
        end_time = time.time()
        profiler.disable()
        
        # Сохранение статистики
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        
        print(f"\n=== Профиль функции: {name} ===")
        print(f"Время выполнения: {end_time - start_time:.4f} секунд")
        stats.print_stats(10)
```

### Отладочные скрипты

#### Скрипт диагностики системы

```bash
#!/bin/bash
# debug_system.sh

echo "=== Система диагностики Compute Network ==="
echo "Время: $(date)"
echo "==========================================="

# Проверка статуса сервиса
echo "1. Проверка статуса сервиса:"
systemctl status compute-network --no-pager

# Проверка портов
echo -e "\n2. Проверка открытых портов:"
netstat -tuln | grep -E '5557|8080'

# Проверка памяти
echo -e "\n3. Проверка использования памяти:"
free -h

# Проверка диска
echo -e "\n4. Проверка дискового пространства:"
df -h

# Проверка CPU
echo -e "\n5. Проверка использования CPU:"
top -bn1 | head -20

# Проверка логов
echo -e "\n6. Последние 10 строк логов:"
tail -n 10 /opt/compute-network/logs/compute_network_$(date +%Y%m%d).log

# Проверка сетевой активности
echo -e "\n7. Проверка сетевой активности:"
ss -tuln | grep -E '5557|8080'

echo -e "\n=== Диагностика завершена ==="
```

#### Скрипт анализа логов

```python
#!/usr/bin/env python3
# analyze_logs.py

import re
import json
from collections import defaultdict
from datetime import datetime, timedelta

class LogAnalyzer:
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.patterns = {
            'error': r'ERROR|error|Error',
            'warning': r'WARNING|warning|Warning',
            'task': r'Task.*?(\w+)',
            'node': r'Node.*?(\w+)',
            'performance': r'(\d+\.\d+)ms'
        }
        
    def analyze_logs(self, hours: int = 24):
        """Анализ логов за последние N часов"""
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        results = defaultdict(list)
        
        with open(self.log_file, 'r') as f:
            for line in f:
                try:
                    timestamp_str = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                    if timestamp_str:
                        timestamp = datetime.strptime(timestamp_str.group(1), '%Y-%m-%d %H:%M:%S')
                        if timestamp >= cutoff_time:
                            self._process_line(line, results)
                except Exception as e:
                    print(f"Ошибка обработки строки: {e}")
                    
        return self._generate_report(results)
        
    def _process_line(self, line: str, results: dict):
        """Обработка строки лога"""
        
        for category, pattern in self.patterns.items():
            matches = re.findall(pattern, line, re.IGNORECASE)
            if matches:
                results[category].extend(matches)
                
    def _generate_report(self, results: dict):
        """Генерация отчета"""
        
        report = {
            'analysis_time': datetime.now().isoformat(),
            'time_range': 'last_24_hours',
            'categories': {}
        }
        
        for category, items in results.items():
            report['categories'][category] = {
                'count': len(items),
                'items': list(set(items))[:10]  # Уникальные элементы
            }
            
        return report

# Использование
if __name__ == "__main__":
    analyzer = LogAnalyzer('/opt/compute-network/logs/compute_network.log')
    report = analyzer.analyze_logs()
    
    print(json.dumps(report, indent=2))
```

---

## 🎯 Заключение

Эта документация охватывает все аспекты развертывания и эксплуатации децентрализованной P2P вычислительной сети:

- ✅ **Развертывание** - от локальной разработки до промышленного масштаба
- ✅ **Мониторинг** - Prometheus, Grafana, кастомные метрики
- ✅ **Логирование** - структурированные логи, ротация, анализ
- ✅ **Обновление** - безопасное обновление, миграция, откат
- ✅ **Безопасность** - SSL, фаервол, мониторинг угроз
- ✅ **Производительность** - оптимизация, профилирование, нагрузочное тестирование
- ✅ **Отладка** - инструменты диагностики, анализ логов

Система готова к эксплуатации в производственной среде и обеспечивает высокую доступность, безопасность и производительность.

🚀 **Готово к запуску в продакшене!**