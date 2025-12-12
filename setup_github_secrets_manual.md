# Настройка GitHub Secrets для CI/CD деплоя

## Что нужно сделать

### 1. Добавить SSH ключ на сервер

Сначала нужно добавить публичный ключ на сервер:

```bash
# Скопируйте этот публичный ключ
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHQKxqx4DihaZSlUlev2RTb7RjVlpjzoTjITATkRSv+9 ariel@rms

# Подключитесь к серверу и добавьте ключ
ssh ariel@185.244.212.194
# На сервере выполните:
mkdir -p ~/.ssh
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHQKxqx4DihaZSlUlev2RTb7RjVlpjzoTjITATkRSv+9 ariel@rms" >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

### 2. Настроить GitHub Secrets

Перейдите в ваш репозиторий: https://github.com/ari3lYT/p2pnet

Settings → Secrets and variables → Actions → New repository secret

Добавьте следующие секреты:

#### SSH_PRIVATE_KEY
```bash
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACB0CsaseA4oWmUpVJXr9kU2+0Y1ZaY86E4yEwE5EUr/vQAAAJC22v+ottr/
qAAAAAtzc2gtZWQyNTUxOQAAACB0CsaseA4oWmUpVJXr9kU2+0Y1ZaY86E4yEwE5EUr/vQ
AAAEABX8N4LdoZF+JvC0z4/02tnFUV0k1pted0GC9VQoiJ1nQKxqx4DihaZSlUlev2RTb7
RjVlpjzoTjITATkRSv+9AAAACWFyaWVsQHJtcwECAwQ=
-----END OPENSSH PRIVATE KEY-----
```

#### SERVER_USER
```
ariel
```

#### SERVER_HOST
```
185.244.212.194
```

#### SERVER_PATH
```
/var/www/p2pnet
```

### 3. Проверить деплой

После настройки секретов сделайте коммит в main ветку, и CI/CD пайплайн автоматически запустится с деплоем.

### 4. Альтернативный вариант: Создать токен GitHub

Если хотите использовать токен вместо SSH ключа:

1. Перейдите в GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Создайте токен с правами `repo` и `workflow`
3. Добавьте секрет `GITHUB_TOKEN` с этим токеном
4. Измените `.github/workflows/ci.yml` для использования HTTPS вместо SSH

### 5. Проверить статус пайплайна

После настройки секретов проверьте статус пайплайна:
https://github.com/ari3lYT/p2pnet/actions