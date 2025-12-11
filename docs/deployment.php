<?php
$title = "Развертывание";
$active = "deployment.php";
$breadcrumbs = [
    ["label" => "Главная", "href" => "index.php"],
    ["label" => "Развертывание"],
];
include __DIR__ . "/layout/header.php";
?>
<section>
    <h2>Узлы (координатор/воркеры)</h2>
    <ul>
        <li>Python 3.11+, psutil; для GPU — GPUtil и драйверы</li>
        <li>Контейнеризация: python:3.11-slim, доступ к docker (для container sandbox)</li>
        <li>Wasm: wasmtime CLI при необходимости</li>
    </ul>
</section>
<section>
    <h2>Документация (FastPanel/nginx/apache)</h2>
    <ul>
        <li>Документ-рут: <code>docs/</code>, индекс <code>docs/index.php</code></li>
        <li>nginx: <code>root /path/to/project/docs;</code> <code>index index.php;</code></li>
        <li>apache: mod_php или php-fpm, DocumentRoot = docs</li>
    </ul>
</section>
<section>
    <h2>Мини-Compose для координатора (пример)</h2>
    <pre><code class="language-yaml">services:
  coordinator:
    image: python:3.11-slim
    volumes: [".:/app"]
    working_dir: /app
    command: ["bash", "-c", "pip install -r requirements.txt && PYTHONPATH=src python src/main.py --host 0.0.0.0 --port 5555"]
    ports: ["5555:5555"]
</code></pre>
    <p class="muted">Добавьте TLS/мTLS, healthchecks, ресурсы cgroups в реальных окружениях.</p>
</section>
<section>
    <h2>Вариант nginx + php-fpm для доков</h2>
    <pre><code class="language-nginx">server {
    listen 80;
    server_name d2omg.ru;
    root /var/www/fastuser/data/www/d2omg.ru/p2p/docs;
    index index.php;

    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    location ~ \.php$ {
        include fastcgi_params;
        fastcgi_pass unix:/run/php/php8.2-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
}
}</code></pre>
</section>

<section>
    <h2>Чек-лист прод-развертывания</h2>
    <ul>
        <li>Подготовить окружение: Python 3.11+, docker/wasmtime, доступ к GPU (опционально)</li>
        <li>Настроить sandbox: container/wasm, лимиты CPU/RAM, отключить сеть в контейнерах</li>
        <li>Настроить TLS/mTLS на транспортном уровне (обвязка поверх InMemoryTransport)</li>
        <li>Метрики: подключить Prometheus scrape <code>/metrics_prom</code></li>
        <li>Логи: централизованный сбор (EFK/Loki), включить DEBUG на стейдже</li>
        <li>CI/CD: прогон ruff/black/pytest+cov, smoke после выката</li>
        <li>Бэкапы конфигов/ключей, ротация секретов</li>
    </ul>
</section>

<section>
    <h2>Подготовка воркеров</h2>
    <ul>
        <li>Разделить воркеры по профилю: CPU-only, GPU, high-mem</li>
        <li>Ограничить ресурсы через cgroups/docker run <code>--memory/--cpus</code></li>
        <li>Проверить доступность sandbox self-test (process/container/wasm)</li>
        <li>Установить agent (ComputeNode) и зарегистрировать у координатора</li>
    </ul>
</section>
<?php include __DIR__ . "/layout/footer.php"; ?>
