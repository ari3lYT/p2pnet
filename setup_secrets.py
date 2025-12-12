#!/usr/bin/env python3
"""
Скрипт для настройки GitHub Secrets через GitHub API
"""

import requests
import json
import os

# Настройки
REPO = "ari3lYT/p2pnet"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

# Секреты для настройки
SECRETS = {
    "SERVER_USER": "root",
    "SERVER_HOST": "d2omg.ru",
    "SERVER_PATH": "/var/www/p2pnet",
    "SSH_PRIVATE_KEY": """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACDy8LukT8aXmzwrlXdc2R4ZtBj8GA3aIHt0XUQYXHHEzgAAAKDsyKKC7Mii
ggAAAAtzc2gtZWQyNTUxOQAAACDy8LukT8aXmzwrlXdc2R4ZtBj8GA3aIHt0XUQYXHHEzg
AAAEBJLwcnekktKzIY7mHo/NAQ0WEPxVCp318Xh66wgQRP/vLwu6RPxpebPCuVd1zZHhm0
GPwYDdoge3RdRBhcccTOAAAAGGdpdGh1Yi1kZXBsb3kta2V5QHAycG5ldAECAwQF
-----END OPENSSH PRIVATE KEY-----"""
}

def set_github_secret(secret_name, secret_value):
    """Установка GitHub secret через API"""
    url = f"https://api.github.com/repos/{REPO}/actions/secrets/{secret_name}"
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Кодируем значение в base64
    import base64
    secret_bytes = secret_value.encode('utf-8')
    encoded_secret = base64.b64encode(secret_bytes).decode('utf-8')
    
    payload = {
        "encrypted_value": encoded_secret,
        "key_id": "your_key_id_here"  # Нужно заменить на реальный key_id
    }
    
    response = requests.put(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        print(f"✅ Секрет {secret_name} успешно установлен")
    else:
        print(f"❌ Ошибка установки секрета {secret_name}: {response.status_code}")
        print(response.text)

def main():
    print("Настройка GitHub Secrets для CI/CD деплоя...")
    
    if not GITHUB_TOKEN:
        print("❌ Ошибка: GITHUB_TOKEN не установлен")
        print("Установите переменную окружения: export GITHUB_TOKEN=your_token_here")
        return
    
    print(f"Репозиторий: {REPO}")
    print("Настройка секретов:")
    
    for secret_name, secret_value in SECRETS.items():
        print(f"  - {secret_name}")
        set_github_secret(secret_name, secret_value)
    
    print("\n🎉 Настройка завершена!")
    print("Теперь нужно:")
    print("1. Добавить публичный SSH ключ на сервер")
    print("2. Проверить работу CI/CD пайплайна")

if __name__ == "__main__":
    main()