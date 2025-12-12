# Обновление GitHub Secrets для правильного сервера

## 🔄 Нужно обновить секреты в GitHub

Перейдите в ваш репозиторий: https://github.com/ari3lYT/p2pnet

Settings → Secrets and variables → Actions → Repository secrets

### Обновите следующие секреты:

#### SERVER_USER
```
root
```

#### SERVER_HOST  
```
d2omg.ru
```

#### SERVER_PATH
```
/var/www/p2pnet
```

#### SSH_PRIVATE_KEY
```bash
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACDy8LukT8aXmzwrlXdc2R4ZtBj8GA3aIHt0XUQYXHHEzgAAAKDsyKKC7Mii
ggAAAAtzc2gtZWQyNTUxOQAAACDy8LukT8aXmzwrlXdc2R4ZtBj8GA3aIHt0XUQYXHHEzg
AAAEBJLwcnekktKzIY7mHo/NAQ0WEPxVCp318Xh66wgQRP/vLwu6RPxpebPCuVd1zZHhm0
GPwYDdoge3RdRBhcccTOAAAAGGdpdGh1Yi1kZXBsb3kta2V5QHAycG5ldAECAwQF
-----END OPENSSH PRIVATE KEY-----
```

## ✅ Что уже сделано:

1. **SSH ключ добавлен на сервер** - ключ `github_deploy_key` успешно добавлен на `root@d2omg.ru`
2. **CI/CD пайплайн готов** - после обновления секретов пайплайн будет работать правильно

## 🚀 После обновления секретов:

1. Сделайте коммит в main ветку
2. CI/CD пайплайн автоматически запустится
3. После успешной проверки всех этапов, произойдет деплой на сервер `d2omg.ru`

## 📊 Проверить статус пайплайна:

https://github.com/ari3lYT/p2pnet/actions

## 🔍 Прогноз:

После обновления секретов пайплайн должен успешно пройти все этапы и выполнить деплой на сервер `d2omg.ru`.