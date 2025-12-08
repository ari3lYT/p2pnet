#!/usr/bin/env python3
"""
Простое P2P приложение на Python
Легко разворачивается и работает без дополнительных зависимостей
"""

import socket
import threading
import json
import time
import argparse
import sys
import os
import random
import struct
import hashlib
import base64
import uuid
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

class P2PNode:
    def __init__(self, host: str = '0.0.0.0', port: int = 5555, bootstrap_hosts: List[str] = None, auto_connect: bool = True):
        self.host = host
        self.port = port
        self.bootstrap_hosts = bootstrap_hosts or []
        self.peers: Dict[str, socket.socket] = {}
        self.known_peers: List[str] = []  # Список известных узлов для восстановления сети
        self.message_queue = []
        self.running = False
        self.server_socket = None
        self.reconnect_timer = None
        self.auto_connect = auto_connect
        self.network_discovery = NetworkDiscovery(self)
        
    def start_server(self):
        """Запускает сервер для приема подключений"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        print(f"🚀 Сервер запущен на {self.host}:{self.port}")
        
        # Запускаем отдельный поток для приема подключений
        accept_thread = threading.Thread(target=self.accept_connections)
        accept_thread.daemon = True
        accept_thread.start()
        
        # Автоматическое подключение к сети
        if self.auto_connect:
            self.auto_connect_to_network()
        
        # Запускаем автоматическое восстановление сети
        self.start_network_recovery()
    
    def accept_connections(self):
        """Принимает входящие подключения"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                peer_id = f"{address[0]}:{address[1]}"
                
                # Запускаем отдельный поток для обработки каждого клиента
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(client_socket, peer_id)
                )
                client_thread.daemon = True
                client_thread.start()
                
                print(f"🔗 Подключен узел: {peer_id}")
                
            except OSError:
                if self.running:
                    print("❌ Ошибка при приеме подключения")
                break
    
    def handle_client(self, client_socket: socket.socket, peer_id: str):
        """Обрабатывает сообщения от конкретного клиента"""
        try:
            while self.running:
                data = client_socket.recv(4096)
                if not data:
                    break
                
                try:
                    message = json.loads(data.decode('utf-8'))
                    self.process_message(message, peer_id)
                except json.JSONDecodeError:
                    print(f"⚠️  Некорректное сообщение от {peer_id}")
                    
        except Exception as e:
            print(f"❌ Ошибка обработки клиента {peer_id}: {e}")
        finally:
            self.remove_peer(peer_id)
            client_socket.close()
    
    def connect_to_peer(self, host: str, port: int):
        """Подключается к другому узлу"""
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((host, port))
            peer_id = f"{host}:{port}"
            
            # Добавляем в список пиров
            self.peers[peer_id] = peer_socket
            
            # Добавляем в список известных пиров для восстановления
            if peer_id not in self.known_peers:
                self.known_peers.append(peer_id)
            
            # Запускаем обработчик для этого пира
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(peer_socket, peer_id)
            )
            client_thread.daemon = True
            client_thread.start()
            
            print(f"🔗 Подключен к узлу: {peer_id}")
            
            # Отправляем сообщение о подключении и запрашиваем список пиров
            self.send_message({
                'type': 'connection',
                'from': f"{self.host}:{self.port}",
                'message': 'Hello from new peer!',
                'request_peers': True
            })
            
        except Exception as e:
            print(f"❌ Не удалось подключиться к {host}:{port}: {e}")
    
    def send_message(self, message: dict, target_peer: str = None):
        """Отправляет сообщение указанному пиру или всем парам"""
        message_data = json.dumps(message).encode('utf-8')
        
        if target_peer and target_peer in self.peers:
            try:
                self.peers[target_peer].send(message_data)
            except Exception as e:
                print(f"❌ Не удалось отправить сообщение {target_peer}: {e}")
                self.remove_peer(target_peer)
        else:
            # Отправляем всем парам
            for peer_id, peer_socket in list(self.peers.items()):
                try:
                    peer_socket.send(message_data)
                except Exception as e:
                    print(f"❌ Не удалось отправить сообщение {peer_id}: {e}")
                    self.remove_peer(peer_id)
    
    def process_message(self, message: dict, peer_id: str):
        """Обрабатывает полученное сообщение"""
        msg_type = message.get('type', 'unknown')
        
        if msg_type == 'connection':
            print(f"📨 Сообщение от {peer_id}: {message.get('message', 'No message')}")
            
            # Если запрошен список пиров, отправляем его
            if message.get('request_peers'):
                peer_list = list(self.known_peers)
                self.send_message({
                    'type': 'peer_list',
                    'from': f"{self.host}:{self.port}",
                    'peers': peer_list
                }, peer_id)
                
        elif msg_type == 'chat':
            print(f"💬 [{peer_id}] {message.get('message', 'No message')}")
            
        elif msg_type == 'ping':
            self.send_message({
                'type': 'pong',
                'from': f"{self.host}:{self.port}",
                'timestamp': time.time()
            }, peer_id)
            
        elif msg_type == 'pong':
            print(f"🏓 Pong получен от {peer_id}")
            
        elif msg_type == 'peer_list':
            # Получаем список пиров и пытаемся подключиться к ним
            new_peers = message.get('peers', [])
            for peer_address in new_peers:
                if peer_address not in self.peers and peer_address not in self.known_peers:
                    try:
                        host, port = peer_address.split(':')
                        self.connect_to_peer(host, int(port))
                    except ValueError:
                        continue
                        
        else:
            print(f"⚠️  Неизвестный тип сообщения: {msg_type}")
    
    def remove_peer(self, peer_id: str):
        """Удаляет пира из списка"""
        if peer_id in self.peers:
            try:
                self.peers[peer_id].close()
            except:
                pass
            del self.peers[peer_id]
            print(f"🔌 Отключен узел: {peer_id}")
            
            # Запускаем восстановление сети при потере подключения
            self.schedule_network_recovery()
    
    def send_chat_message(self, text: str):
        """Отправляет текстовое сообщение всем парам"""
        message = {
            'type': 'chat',
            'from': f"{self.host}:{self.port}",
            'timestamp': time.time(),
            'message': text
        }
        self.send_message(message)
    
    def ping_all(self):
        """Отправляет ping всем парам"""
        message = {
            'type': 'ping',
            'from': f"{self.host}:{self.port}",
            'timestamp': time.time()
        }
        self.send_message(message)
    
    def list_peers(self):
        """Выводит список активных пиров"""
        if not self.peers:
            print("🔍 Нет активных пиров")
        else:
            print("🔍 Активные пиры:")
            for peer_id in self.peers:
                print(f"  • {peer_id}")
    
    def start_network_recovery(self):
        """Запускает периодическое восстановление сети"""
        if self.running and len(self.peers) < 2:
            self.reconnect_network()
        
        # Запускаем восстановление каждые 30 секунд
        if self.reconnect_timer:
            self.reconnect_timer.cancel()
        
        self.reconnect_timer = threading.Timer(30.0, self.start_network_recovery)
        self.reconnect_timer.daemon = True
        self.reconnect_timer.start()
    
    def schedule_network_recovery(self):
        """Планирует немедленное восстановление сети"""
        if self.reconnect_timer:
            self.reconnect_timer.cancel()
        
        self.reconnect_timer = threading.Timer(5.0, self.reconnect_network)
        self.reconnect_timer.daemon = True
        self.reconnect_timer.start()
    
    def reconnect_network(self):
        """Пытается восстановить сеть, подключаясь к известным узлам"""
        if not self.running:
            return
            
        # Если нет активных пиров, пытаемся подключиться к известным узлам
        if len(self.peers) == 0 and self.known_peers:
            print("🔄 Попытка восстановления сети...")
            
            for peer_address in self.known_peers[:]:  # Копируем список для безопасного удаления
                if peer_address not in self.peers:
                    try:
                        host, port = peer_address.split(':')
                        self.connect_to_peer(host, int(port))
                        # После успешного подключения выходим, чтобы не создавать слишком много соединений
                        break
                    except (ValueError, Exception):
                        self.known_peers.remove(peer_address)
                        continue
        
        # Если нет известных пиров, но есть bootstrap узлы, пробуем их
        elif len(self.peers) == 0 and self.bootstrap_hosts:
            print("🔄 Попытка подключения к bootstrap узлам...")
            for bootstrap_host in self.bootstrap_hosts:
                try:
                    host, port = bootstrap_host.split(':')
                    self.connect_to_peer(host, int(port))
                    break
                except ValueError:
                    continue
    
    def stop(self):
        """Останавливает работу узла"""
        self.running = False
        if self.reconnect_timer:
            self.reconnect_timer.cancel()
            
        if self.server_socket:
            self.server_socket.close()
        
        # Закрываем все подключения с парами
        for peer_socket in self.peers.values():
            try:
                peer_socket.close()
            except:
                pass
        
        self.peers.clear()
        print("🛑 Сервер остановлен")

def main():
    parser = argparse.ArgumentParser(description='Simple P2P Chat Application')
    parser.add_argument('--host', default='0.0.0.0', help='Host address')
    parser.add_argument('--port', type=int, default=5555, help='Port number')
    parser.add_argument('--bootstrap', nargs='+', help='Bootstrap hosts to connect to (format: host:port)')
    
    args = parser.parse_args()
    
    # Создаем и запускаем узел
    bootstrap_hosts = args.bootstrap or []
    node = P2PNode(args.host, args.port, bootstrap_hosts)
    
    try:
        node.start_server()
        
        print("\n🎯 Доступные команды:")
        print("  send <text>   - отправить сообщение")
        print("  ping          - отправить ping всем парам")
        print("  list          - показать список пиров")
        print("  help          - показать эту справку")
        print("  quit          - выйти из приложения")
        print("-" * 40)
        
        while True:
            try:
                command = input("> ").strip()
                
                if not command:
                    continue
                    
                parts = command.split(' ', 1)
                cmd = parts[0].lower()
                
                if cmd == 'send' and len(parts) > 1:
                    node.send_chat_message(parts[1])
                    
                elif cmd == 'ping':
                    node.ping_all()
                    
                elif cmd == 'list':
                    node.list_peers()
                    
                elif cmd == 'help':
                    print("\n🎯 Доступные команды:")
                    print("  send <text>   - отправить сообщение")
                    print("  ping          - отправить ping всем парам")
                    print("  list          - показать список пиров")
                    print("  help          - показать эту справку")
                    print("  quit          - выйти из приложения")
                    
                elif cmd in ['quit', 'exit']:
                    break
                    
                else:
                    print("❌ Неизвестная команда. Введите 'help' для справки")
                    
            except KeyboardInterrupt:
                break
            except EOFError:
                break
                
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
    finally:
        node.stop()

class NetworkDiscovery:
    """Класс для автоматического обнаружения сетей (локальных и глобальных)"""
    
    def __init__(self, node):
        self.node = node
        self.discovery_port = 5556  # Порт для discovery broadcast
        self.broadcast_interval = 10  # Интервал отправки broadcast сообщений
        self.last_broadcast = 0
        self.global_discovery = GlobalDiscovery(node)
        
    def start_discovery(self):
        """Запускает автоматическое обнаружение сетей"""
        # Запускаем UDP broadcast для обнаружения сетей
        discovery_thread = threading.Thread(target=self.udp_discovery)
        discovery_thread.daemon = True
        discovery_thread.start()
        
        # Запускаем поиск в локальной подсети
        subnet_thread = threading.Thread(target=self.subnet_scan)
        subnet_thread.daemon = True
        subnet_thread.start()
        
        # Если включен глобальный режим, запускаем глобальное обнаружение
        if hasattr(self.node, 'global_mode') and self.node.global_mode:
            print("🌐 Запускаю глобальное обнаружение сетей...")
            self.global_discovery.start()
    
    def udp_discovery(self):
        """UDP broadcast для обнаружения сетей"""
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.settimeout(1)
        
        while self.node.running:
            try:
                # Отправляем сообщение о существовании нашей сети
                message = {
                    'type': 'network_announce',
                    'node': f"{self.node.host}:{self.node.port}",
                    'timestamp': time.time()
                }
                udp_socket.sendto(json.dumps(message).encode(), ('255.255.255.255', self.discovery_port))
                print("📡 Отправляю broadcast для обнаружения сетей...")
                
                # Проверяем incoming messages
                try:
                    data, addr = udp_socket.recvfrom(1024)
                    received_msg = json.loads(data.decode())
                    
                    if received_msg.get('type') == 'network_announce':
                        peer_address = received_msg.get('node')
                        if peer_address and peer_address != f"{self.node.host}:{self.node.port}":
                            if peer_address not in self.node.peers:
                                print(f"🔍 Обнаружен узел: {peer_address}")
                                host, port = peer_address.split(':')
                                self.node.connect_to_peer(host, int(port))
                
                except socket.timeout:
                    pass
                    
            except Exception as e:
                print(f"⚠️  Ошибка в UDP discovery: {e}")
            
            time.sleep(self.broadcast_interval)
    
    def subnet_scan(self):
        """Сканирование локальной подсети на наличие узлов"""
        while self.node.running:
            try:
                # Получаем локальный IP диапазон
                local_ip = socket.gethostbyname(socket.gethostname())
                network = '.'.join(local_ip.split('.')[:-1]) + '.'
                
                # Проверяем несколько случайных адресов в подсети
                for i in range(5):
                    ip = network + str(random.randint(1, 254))
                    port = self.node.port
                    
                    try:
                        # Пытаемся подключиться
                        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        test_socket.settimeout(2)
                        result = test_socket.connect_ex((ip, port))
                        
                        if result == 0:
                            peer_address = f"{ip}:{port}"
                            if peer_address not in self.node.peers:
                                print(f"🔍 Обнаружен узел через сканирование: {peer_address}")
                                self.node.connect_to_peer(ip, port)
                        
                        test_socket.close()
                    except:
                        continue
                        
            except Exception as e:
                print(f"⚠️  Ошибка при сканировании подсети: {e}")
            
            time.sleep(30)  # Сканируем каждые 30 секунд

def auto_connect_to_network(node):
    """Автоматическое подключение к существующей сети"""
    print("🔍 Автоматический поиск сетей...")
    
    # Сначала пробуем bootstrap узлы
    if node.bootstrap_hosts:
        print("🌐 Пробую подключиться к bootstrap узлам...")
        for bootstrap_host in node.bootstrap_hosts:
            try:
                host, port = bootstrap_host.split(':')
                print(f"   📍 Пытаюсь: {host}:{port}")
                node.connect_to_peer(host, int(port))
                print(f"✅ Подключен к bootstrap узлу: {bootstrap_host}")
                return
            except ValueError:
                print(f"   ⚠️  Некорректный формат: {bootstrap_host}")
                continue
            except Exception as e:
                print(f"   ❌ Не удалось подключиться к {bootstrap_host}: {e}")
                continue
    
    # Запускаем discovery
    print("📡 Запускаю сетевое обнаружение...")
    node.network_discovery.start_discovery()
    
    # Ждем и пробуем подключиться
    print("⏳ Жду обнаружения узлов...")
    time.sleep(5)
    
    if not node.peers:
        print("🔄 Пробую найти узлы в локальной сети...")
        # Discovery уже запущен, просто ждем
        time.sleep(10)
    
    if node.peers:
        print(f"✅ Автоматически подключено к {len(node.peers)} узлам")
        print("🌍 Сеть активна! Можете отправлять сообщения.")
    else:
        print("⚠️  Не удалось автоматически найти сеть.")
        print("💡 Попробуйте:")
        print("   1. Запустить с --global-mode для глобального поиска")
        print("   2. Указать конкретные узлы: --bootstrap host:port")
        print("   3. Создать новую сеть самостоятельно")

def main():
    parser = argparse.ArgumentParser(description='Simple P2P Chat Application')
    parser.add_argument('--host', default='0.0.0.0', help='Host address')
    parser.add_argument('--port', type=int, default=5555, help='Port number')
    parser.add_argument('--bootstrap', nargs='+', help='Bootstrap hosts to connect to (format: host:port)')
    parser.add_argument('--no-auto-connect', action='store_true', help='Disable automatic network discovery')
    parser.add_argument('--global-mode', action='store_true', help='Enable global network discovery')
    
    args = parser.parse_args()
    
    # Создаем и запускаем узел
    bootstrap_hosts = args.bootstrap or []
    auto_connect = not args.no_auto_connect
    global_mode = args.global_mode
    
    # Глобальные bootstrap узлы для подключения пользователей со всего мира
    global_bootstrap_hosts = [
        'p2p.network:5555',      # Публичный bootstrap узел
        'node.p2p.chat:5555',    # Альтернативный публичный узел
        '45.67.89.100:5555',    # Пример публичного IP
        'seed.p2p.global:5555', # Глобальный seed узел
    ]
    
    # Если не указаны bootstrap узлы, используем стандартные
    if not bootstrap_hosts and auto_connect:
        if global_mode:
            bootstrap_hosts = global_bootstrap_hosts
        else:
            bootstrap_hosts = [
                '127.0.0.1:5555',  # Локальный хост
                '192.168.1.1:5555',  # Типичный роутер
                '192.168.0.1:5555',  # Альтернативный роутер
            ]
    
    node = P2PNode(args.host, args.port, bootstrap_hosts, auto_connect)
    
    try:
        node.start_server()
        
        # Если включено авто-подключение и нет bootstrap узлов, запускаем поиск
        if auto_connect and not args.bootstrap:
            threading.Thread(target=auto_connect_to_network, args=(node,), daemon=True).start()
        
        print("\n🎯 Доступные команды:")
        print("  send <text>   - отправить сообщение")
        print("  ping          - отправить ping всем парам")
        print("  list          - показать список пиров")
        print("  help          - показать эту справку")
        print("  quit          - выйти из приложения")
        print("-" * 40)
        
        while True:
            try:
                command = input("> ").strip()
                
                if not command:
                    continue
                    
                parts = command.split(' ', 1)
                cmd = parts[0].lower()
                
                if cmd == 'send' and len(parts) > 1:
                    node.send_chat_message(parts[1])
                    
                elif cmd == 'ping':
                    node.ping_all()
                    
                elif cmd == 'list':
                    node.list_peers()
                    
                elif cmd == 'help':
                    print("\n🎯 Доступные команды:")
                    print("  send <text>   - отправить сообщение")
                    print("  ping          - отправить ping всем парам")
                    print("  list          - показать список пиров")
                    print("  help          - показать эту справку")
                    print("  quit          - выйти из приложения")
                    
                elif cmd in ['quit', 'exit']:
                    break
                    
                else:
                    print("❌ Неизвестная команда. Введите 'help' для справки")
                    
            except KeyboardInterrupt:
                break
            except EOFError:
                break
                
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
    finally:
        node.stop()

class GlobalDiscovery:
    """Глобальное обнаружение сетей через публичные серверы и DHT"""
    
    def __init__(self, node):
        self.node = node
        self.public_servers = [
            'p2p-registry.example.com:8080',  # Публичный реестр
            'nodes.p2p.network:8080',        # Глобальная сеть узлов
            'seed-chat.p2p:8080',             # Seed-узлы для чата
        ]
        self.dht_nodes = [
            'dht.p2p.global:5555',           # Глобальный DHT
            'p2p-dht.network:5555',          # Альтернативный DHT
        ]
    
    def start(self):
        """Запускает глобальное обнаружение"""
        # Запускаем запросы к публичным серверам
        for server in self.public_servers:
            threading.Thread(target=self.query_public_server, args=(server,), daemon=True).start()
        
        # Запускаем DHT запросы
        for dht_node in self.dht_nodes:
            threading.Thread(target=self.query_dht_node, args=(dht_node,), daemon=True).start()
        
        # Запускаем定期查询
        threading.Thread(target=self.periodic_global_query, daemon=True).start()
    
    def query_public_server(self, server):
        """Запрашивает список узлов у публичного сервера"""
        try:
            import urllib.request
            import urllib.error
            
            url = f"http://{server}/nodes"
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'P2P-Chat/1.0')
            
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    data = response.read().decode('utf-8')
                    nodes = json.loads(data)
                    
                    for node_address in nodes:
                        if node_address not in self.node.peers:
                            try:
                                host, port = node_address.split(':')
                                self.node.connect_to_peer(host, int(port))
                                print(f"🌍 Подключен к глобальному узлу: {node_address}")
                            except ValueError:
                                continue
                                
            except urllib.error.URLError as e:
                print(f"⚠️  Не удалось запросить публичный сервер {server}: {e}")
                
        except Exception as e:
            print(f"⚠️  Ошибка при запросе к {server}: {e}")
    
    def query_dht_node(self, dht_node):
        """Запрашивает узлы у DHT узла"""
        try:
            host, port = dht_node.split(':')
            
            # Отправляем запрос к DHT узлу
            message = {
                'type': 'dht_query',
                'node_id': self.generate_node_id(),
                'request_peers': True
            }
            
            # Пробуем подключиться и отправить запрос
            try:
                dht_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                dht_socket.settimeout(10)
                dht_socket.connect((host, int(port)))
                
                dht_socket.send(json.dumps(message).encode('utf-8'))
                
                # Ждем ответа
                response_data = dht_socket.recv(4096)
                response = json.loads(response_data.decode('utf-8'))
                
                if response.get('type') == 'dht_response' and 'peers' in response:
                    for peer_address in response['peers']:
                        if peer_address not in self.node.peers:
                            try:
                                peer_host, peer_port = peer_address.split(':')
                                self.node.connect_to_peer(peer_host, int(peer_port))
                                print(f"🌍 DHT: Подключен к узлу: {peer_address}")
                            except ValueError:
                                continue
                
                dht_socket.close()
                
            except Exception as e:
                print(f"⚠️  Не удалось запросить DHT узел {dht_node}: {e}")
                
        except ValueError:
            print(f"⚠️  Некорректный формат DHT узла: {dht_node}")
    
    def generate_node_id(self):
        """Генерирует уникальный ID для узла"""
        import hashlib
        import uuid
        
        unique_string = f"{self.node.host}:{self.node.port}:{uuid.uuid4()}"
        return hashlib.sha256(unique_string.encode()).hexdigest()[:16]
    
    def periodic_global_query(self):
        """Периодический запрос к глобальным сетям"""
        while self.node.running:
            time.sleep(60)  # Запрашиваем каждую минуту
            
            if self.node.global_mode:
                # Повторяем запросы к глобальным серверам
                for server in self.public_servers:
                    threading.Thread(target=self.query_public_server, args=(server,), daemon=True).start()
                
                for dht_node in self.dht_nodes:
                    threading.Thread(target=self.query_dht_node, args=(dht_node,), daemon=True).start()

def auto_connect_to_network(node):
    """Автоматическое подключение к существующей сети"""
    print("🔍 Автоматический поиск сетей...")
    
    # Сначала пробуем bootstrap узлы
    if node.bootstrap_hosts:
        print("🌐 Пробую подключиться к bootstrap узлам...")
        for bootstrap_host in node.bootstrap_hosts:
            try:
                host, port = bootstrap_host.split(':')
                print(f"   📍 Пытаюсь: {host}:{port}")
                node.connect_to_peer(host, int(port))
                print(f"✅ Подключен к bootstrap узлу: {bootstrap_host}")
                return
            except ValueError:
                print(f"   ⚠️  Некорректный формат: {bootstrap_host}")
                continue
            except Exception as e:
                print(f"   ❌ Не удалось подключиться к {bootstrap_host}: {e}")
                continue
    
    # Запускаем discovery
    print("📡 Запускаю сетевое обнаружение...")
    node.network_discovery.start_discovery()
    
    # Ждем и пробуем подключиться
    print("⏳ Жду обнаружения узлов...")
    time.sleep(5)
    
    if not node.peers:
        print("🔄 Пробую найти узлы в локальной сети...")
        # Discovery уже запущен, просто ждем
        time.sleep(10)
    
    if node.peers:
        print(f"✅ Автоматически подключено к {len(node.peers)} узлам")
        print("🌍 Сеть активна! Можете отправлять сообщения.")
    else:
        print("⚠️  Не удалось автоматически найти сеть.")
        print("💡 Попробуйте:")
        print("   1. Запустить с --global-mode для глобального поиска")
        print("   2. Указать конкретные узлы: --bootstrap host:port")
        print("   3. Создать новую сеть самостоятельно")

def main():
    parser = argparse.ArgumentParser(description='Simple P2P Chat Application')
    parser.add_argument('--host', default='0.0.0.0', help='Host address')
    parser.add_argument('--port', type=int, default=5555, help='Port number')
    parser.add_argument('--bootstrap', nargs='+', help='Bootstrap hosts to connect to (format: host:port)')
    parser.add_argument('--no-auto-connect', action='store_true', help='Disable automatic network discovery')
    parser.add_argument('--global-mode', action='store_true', help='Enable global network discovery')
    
    args = parser.parse_args()
    
    # Создаем и запускаем узел
    bootstrap_hosts = args.bootstrap or []
    auto_connect = not args.no_auto_connect
    global_mode = args.global_mode
    
    # Глобальные bootstrap узлы для подключения пользователей со всего мира
    global_bootstrap_hosts = [
        'p2p.network:5555',      # Публичный bootstrap узел
        'node.p2p.chat:5555',    # Альтернативный публичный узел
        '45.67.89.100:5555',    # Пример публичного IP
        'seed.p2p.global:5555', # Глобальный seed узел
    ]
    
    # Если не указаны bootstrap узлы, используем стандартные
    if not bootstrap_hosts and auto_connect:
        if global_mode:
            bootstrap_hosts = global_bootstrap_hosts
        else:
            bootstrap_hosts = [
                '127.0.0.1:5555',  # Локальный хост
                '192.168.1.1:5555',  # Типичный роутер
                '192.168.0.1:5555',  # Альтернативный роутер
            ]
    
    node = P2PNode(args.host, args.port, bootstrap_hosts, auto_connect)
    node.global_mode = global_mode  # Сохраняем глобальный режим
    
    try:
        node.start_server()
        
        # Если включено авто-подключение и нет bootstrap узлов, запускаем поиск
        if auto_connect and not args.bootstrap:
            threading.Thread(target=auto_connect_to_network, args=(node,), daemon=True).start()
        
        print("\n🎯 Доступные команды:")
        print("  send <text>   - отправить сообщение")
        print("  ping          - отправить ping всем парам")
        print("  list          - показать список пиров")
        print("  help          - показать эту справку")
        print("  quit          - выйти из приложения")
        print("-" * 40)
        
        while True:
            try:
                command = input("> ").strip()
                
                if not command:
                    continue
                    
                parts = command.split(' ', 1)
                cmd = parts[0].lower()
                
                if cmd == 'send' and len(parts) > 1:
                    node.send_chat_message(parts[1])
                    
                elif cmd == 'ping':
                    node.ping_all()
                    
                elif cmd == 'list':
                    node.list_peers()
                    
                elif cmd == 'help':
                    print("\n🎯 Доступные команды:")
                    print("  send <text>   - отправить сообщение")
                    print("  ping          - отправить ping всем парам")
                    print("  list          - показать список пиров")
                    print("  help          - показать эту справку")
                    print("  quit          - выйти из приложения")
                    
                elif cmd in ['quit', 'exit']:
                    break
                    
                else:
                    print("❌ Неизвестная команда. Введите 'help' для справки")
                    
            except KeyboardInterrupt:
                break
            except EOFError:
                break
                
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
    finally:
        node.stop()

class CryptoUtils:
    """Утилиты для криптографии"""
    
    @staticmethod
    def generate_keypair():
        """Генерирует пару ключей Ed25519"""
        private_key = ed25519.Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        return private_key, public_key
    
    @staticmethod
    def private_key_to_bytes(private_key):
        """Конвертирует приватный ключ в bytes"""
        return private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
    
    @staticmethod
    def public_key_to_bytes(public_key):
        """Конвертирует публичный ключ в bytes"""
        return public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
    
    @staticmethod
    def bytes_to_private_key(key_bytes):
        """Конвертирует bytes в приватный ключ"""
        return ed25519.Ed25519PrivateKey.from_private_bytes(key_bytes)
    
    @staticmethod
    def bytes_to_public_key(key_bytes):
        """Конвертирует bytes в публичный ключ"""
        return ed25519.Ed25519PublicKey.from_public_bytes(key_bytes)
    
    @staticmethod
    def sign(private_key, message):
        """Подписывает сообщение"""
        return private_key.sign(message)
    
    @staticmethod
    def verify(public_key, signature, message):
        """Проверяет подпись"""
        try:
            public_key.verify(signature, message)
            return True
        except:
            return False

class NodeIdentity:
    """Идентификация узла"""
    
    def __init__(self, role="client", load_existing=True):
        self.role = role  # "seed", "public", "client"
        self.node_id = None
        self.private_key = None
        self.public_key = None
        self.version = "0.3.1"
        
        # Пытаемся загрузить существующие ключи
        if load_existing:
            self.load_keys()
        else:
            self.generate_keys()
    
    def generate_keys(self):
        """Генерирует новую пару ключей"""
        self.private_key, self.public_key = CryptoUtils.generate_keypair()
        self.node_id = base64.b64encode(CryptoUtils.public_key_to_bytes(self.public_key)).decode('utf-8')
    
    def load_keys(self):
        """Загружает ключи из файла"""
        key_file = f"node_{self.role}_private.key"
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                key_bytes = f.read()
                self.private_key = CryptoUtils.bytes_to_private_key(key_bytes)
                self.public_key = self.private_key.public_key()
                self.node_id = base64.b64encode(CryptoUtils.public_key_to_bytes(self.public_key)).decode('utf-8')
        else:
            self.generate_keys()
            self.save_keys()
    
    def save_keys(self):
        """Сохраняет ключи в файл"""
        if self.private_key:
            key_file = f"node_{self.role}_private.key"
            with open(key_file, 'wb') as f:
                f.write(CryptoUtils.private_key_to_bytes(self.private_key))
    
    def sign_message(self, message):
        """Подписывает сообщение"""
        if self.private_key:
            message_bytes = json.dumps(message, sort_keys=True).encode('utf-8')
            signature = CryptoUtils.sign(self.private_key, message_bytes)
            return base64.b64encode(signature).decode('utf-8')
        return None
    
    def verify_message(self, message, signature, public_key_bytes=None):
        """Проверяет подпись сообщения"""
        if public_key_bytes is None:
            public_key_bytes = CryptoUtils.public_key_to_bytes(self.public_key)
        
        try:
            public_key = CryptoUtils.bytes_to_public_key(public_key_bytes)
            message_bytes = json.dumps(message, sort_keys=True).encode('utf-8')
            signature_bytes = base64.b64decode(signature)
            return CryptoUtils.verify(public_key, signature_bytes, message_bytes)
        except:
            return False

class NetworkConfig:
    """Конфигурация сети"""
    
    def __init__(self):
        self.config = {
            "version": 1,
            "min_supported_version": "0.3.0",
            "trusted_seeds": [],
            "revoked_seeds": []
        }
        self.signature = None
    
    def load_from_file(self, filename="network_config.json"):
        """Загружает конфиг из файла"""
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                self.config = data.get('config', self.config)
                self.signature = data.get('sig')
    
    def save_to_file(self, filename="network_config.json"):
        """Сохраняет конфиг в файл"""
        data = {
            "config": self.config,
            "sig": self.signature
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def sign(self, private_key):
        """Подписывает конфиг"""
        config_bytes = json.dumps(self.config, sort_keys=True).encode('utf-8')
        signature = CryptoUtils.sign(private_key, config_bytes)
        self.signature = base64.b64encode(signature).decode('utf-8')
    
    def verify(self, public_key):
        """Проверяет подпись конфига"""
        if not self.signature:
            return False
        
        try:
            public_key_bytes = CryptoUtils.public_key_to_bytes(public_key)
            config_bytes = json.dumps(self.config, sort_keys=True).encode('utf-8')
            signature_bytes = base64.b64decode(self.signature)
            return CryptoUtils.verify(public_key, signature_bytes, config_bytes)
        except:
            return False

class SeedCertificate:
    """Сертификат для seed-узла"""
    
    def __init__(self):
        self.seed_pubkey = None
        self.issued_at = None
        self.expires_at = None
        self.signature = None
    
    def create(self, seed_public_key, root_private_key, expires_at=0):
        """Создает сертификат от имени root"""
        self.seed_pubkey = base64.b64encode(CryptoUtils.public_key_to_bytes(seed_public_key)).decode('utf-8')
        self.issued_at = int(time.time())
        self.expires_at = expires_at
        
        # Создаем данные для подписи
        cert_data = {
            "seed_pubkey": self.seed_pubkey,
            "issued_at": self.issued_at,
            "expires_at": self.expires_at
        }
        
        # Подписываем root-ключом
        cert_bytes = json.dumps(cert_data, sort_keys=True).encode('utf-8')
        self.signature = base64.b64encode(CryptoUtils.sign(root_private_key, cert_bytes)).decode('utf-8')
    
    def verify(self, root_public_key):
        """Проверяет сертификат root-ключом"""
        if not self.signature:
            return False
        
        try:
            cert_data = {
                "seed_pubkey": self.seed_pubkey,
                "issued_at": self.issued_at,
                "expires_at": self.expires_at
            }
            
            cert_bytes = json.dumps(cert_data, sort_keys=True).encode('utf-8')
            signature_bytes = base64.b64decode(self.signature)
            
            return CryptoUtils.verify(root_public_key, signature_bytes, cert_bytes)
        except:
            return False

class P2PNode:
    def __init__(self, host: str = '0.0.0.0', port: int = 5555, bootstrap_hosts: List[str] = None, auto_connect: bool = True, role: str = "client"):
        self.host = host
        self.port = port
        self.bootstrap_hosts = bootstrap_hosts or []
        self.peers: Dict[str, socket.socket] = {}
        self.known_peers: List[str] = []  # Список известных узлов для восстановления сети
        self.message_queue = []
        self.running = False
        self.server_socket = None
        self.reconnect_timer = None
        self.auto_connect = auto_connect
        self.network_discovery = NetworkDiscovery(self)
        
        # Новые компоненты
        self.identity = NodeIdentity(role)
        self.network_config = NetworkConfig()
        self.seed_certificate = None
        
        # Root публичный ключ (вшивается в клиент)
        self.root_public_key = None
        
        # Доверенные seed-узлы
        self.SEED_ADDRESSES = [
            "d2omg.ru:6666"  # Единственный доверенный seed
        ]
        
        # Загружаем конфиг сети
        self.network_config.load_from_file()
        
        # Если это seed-режим, создаем сертификат
        if role == "seed":
            self.create_seed_certificate()
            self.setup_trusted_network()
    
    def create_seed_certificate(self):
        """Создает сертификат для seed-узла"""
        # Загружаем root-ключ
        root_private_key = self.load_root_private_key()
        if root_private_key:
            self.seed_certificate = SeedCertificate()
            self.seed_certificate.create(self.identity.public_key, root_private_key)
            print("✅ Seed сертификат создан")
    
    def load_root_private_key(self):
        """Загружает root приватный ключ"""
        if os.path.exists("root_private.key"):
            with open("root_private.key", 'rb') as f:
                key_bytes = f.read()
                return CryptoUtils.bytes_to_private_key(key_bytes)
        return None
    
    def setup_trusted_network(self):
        """Настраивает доверенную сеть с d2omg.ru:6666"""
        # Создаем root-ключ если его нет
        if not os.path.exists("root_private.key"):
            print("🔑 Генерирую root-ключ для доверенной сети...")
            root_priv, root_pub = CryptoUtils.generate_keypair()
            with open("root_private.key", 'wb') as f:
                f.write(CryptoUtils.private_key_to_bytes(root_priv))
            
            # Сохраняем публичный ключ для клиентов
            root_pub_bytes = CryptoUtils.public_key_to_bytes(root_pub)
            with open("root_public.key", 'w') as f:
                f.write(base64.b64encode(root_pub_bytes).decode('utf-8'))
            
            print("✅ Root-ключ сгенерирован и сохранен")
        
        # Настраиваем конфигурацию сети с d2omg.ru:6666 как единственным trusted seed
        self.network_config.config = {
            "version": 1,
            "min_supported_version": "0.3.1",
            "trusted_seeds": [
                {
                    "pubkey": self.get_seed_pubkey(),
                    "addr": "d2omg.ru:6666"
                }
            ],
            "revoked_seeds": []
        }
        
        # Подписываем конфигурацию root-ключом
        root_priv = self.load_root_private_key()
        if root_priv:
            self.network_config.sign(root_priv)
            self.network_config.save_to_file()
            print("✅ Конфигурация доверенной сети подписана и сохранена")
    
    def get_seed_pubkey(self):
        """Получает публичный ключ seed-узла"""
        if self.identity.public_key:
            return base64.b64encode(CryptoUtils.public_key_to_bytes(self.identity.public_key)).decode('utf-8')
        return None

class HandshakeProtocol:
    """Протокол рукопожатия"""
    
    @staticmethod
    def create_handshake_message(identity):
        """Создает сообщение для рукопожатия"""
        return {
            "type": "handshake",
            "node_pubkey": identity.node_id,
            "role": identity.role,
            "version": identity.version,
            "timestamp": time.time()
        }
    
    @staticmethod
    def validate_handshake(message, identity):
        """Проверяет сообщение рукопожатия"""
        required_fields = ["type", "node_pubkey", "role", "version", "timestamp"]
        
        for field in required_fields:
            if field not in message:
                return False
        
        # Проверяем версию
        if message["version"] < identity.network_config.config["min_supported_version"]:
            return False
        
        # Проверяем роль
        valid_roles = ["seed", "public", "client"]
        if message["role"] not in valid_roles:
            return False
        
        return True

# ... остальной код остается без изменений ...