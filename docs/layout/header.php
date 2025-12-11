<?php
$title = $title ?? "WF P2P Compute Docs";
$active = $active ?? "";
$breadcrumbs = $breadcrumbs ?? [];
$navTree = [
    ["href" => "index.php", "label" => "Обзор"],
    ["href" => "quickstart.php", "label" => "Быстрый старт"],
    ["href" => "architecture.php", "label" => "Архитектура"],
    ["href" => "tasks.php", "label" => "Задачи & Privacy"],
    ["href" => "pipeline.php", "label" => "Pipeline/DAG"],
    ["href" => "sandbox.php", "label" => "Sandbox"],
    ["href" => "protocol.php", "label" => "Протокол/Транспорт"],
    ["href" => "scheduler.php", "label" => "Планировщик/Jobs"],
    ["href" => "deployment.php", "label" => "Развертывание"],
    ["href" => "security.php", "label" => "Безопасность"],
    ["href" => "monitoring.php", "label" => "Мониторинг"],
    ["href" => "testing.php", "label" => "Тесты/CI"],
    ["href" => "api.php", "label" => "API/Swagger"],
    ["href" => "faq.php", "label" => "FAQ"],
];
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title><?= htmlspecialchars($title) ?></title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
    <script>
        tailwind.config = {
          theme: {
            extend: {
              colors: {
                brand: "#38bdf8",
                surface: "#0b1220",
                panel: "#0f172a",
              }
            }
          }
        }
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({startOnLoad:true, theme: "dark"});</script>
</head>
<body class="bg-surface text-slate-100 min-h-screen flex">
    <aside class="hidden lg:flex flex-col w-72 bg-panel border-r border-slate-800 sticky top-0 h-screen overflow-y-auto">
        <div class="p-4 border-b border-slate-800">
            <div class="text-xs uppercase tracking-widest text-slate-400 mb-1">Документация</div>
            <div class="text-lg font-semibold text-white">WF P2P Compute</div>
            <div class="mt-2 text-xs text-slate-400">Prod-grade P2P вычислительная сеть</div>
        </div>
        <nav class="flex-1 p-3 space-y-1 text-sm">
            <?php foreach ($navTree as $item): ?>
                <a href="<?= $item["href"] ?>" class="flex items-center gap-2 px-3 py-2 rounded-lg border <?= $active === $item["href"] ? 'border-brand text-brand bg-slate-900/60' : 'border-transparent text-slate-200 hover:border-brand/50 hover:text-brand' ?>">
                    <?= $item["label"] ?>
                </a>
            <?php endforeach; ?>
        </nav>
        <div class="p-3 border-t border-slate-800 text-xs text-slate-400">
            <p>Статус: <span class="text-green-400">Стабильно</span></p>
            <p>Покрытие тестами: 90%</p>
            <p>Sandbox: process/container/wasm</p>
        </div>
    </aside>
    <div class="flex-1 flex flex-col min-h-screen">
        <header class="sticky top-0 z-20 bg-surface/90 backdrop-blur border-b border-slate-800">
            <div class="max-w-7xl mx-auto px-4 py-3 flex flex-col gap-2">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-xs uppercase tracking-widest text-slate-400">Документация</p>
                        <h1 class="text-xl font-semibold text-white"><?= htmlspecialchars($title) ?></h1>
                        <?php if (!empty($breadcrumbs)): ?>
                            <div class="text-xs text-slate-400 mt-1">
                                <?php foreach ($breadcrumbs as $i => $crumb): ?>
                                    <?php if ($i > 0): ?> / <?php endif; ?>
                                    <?php if (!empty($crumb['href'])): ?>
                                        <a href="<?= $crumb['href'] ?>" class="hover:text-brand"><?= htmlspecialchars($crumb['label']) ?></a>
                                    <?php else: ?>
                                        <span><?= htmlspecialchars($crumb['label']) ?></span>
                                    <?php endif; ?>
                                <?php endforeach; ?>
                            </div>
                        <?php endif; ?>
                    </div>
                    <div class="hidden md:flex gap-2 text-xs text-slate-400">
                        <span class="px-2 py-1 rounded bg-slate-800 border border-slate-700">Prod-ready</span>
                        <span class="px-2 py-1 rounded bg-slate-800 border border-slate-700">Privacy</span>
                        <span class="px-2 py-1 rounded bg-slate-800 border border-slate-700">Sandbox</span>
                    </div>
                </div>
            </div>
        </header>
        <main class="max-w-6xl mx-auto px-4 py-10 prose prose-invert prose-slate">
