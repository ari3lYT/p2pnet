        </main>
    </div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
<script>
    // Добавляем кнопки "Скопировать" ко всем блокам кода
    document.querySelectorAll('pre > code').forEach((codeBlock) => {
        const pre = codeBlock.parentNode;
        pre.classList.add("relative", "group");
        const button = document.createElement('button');
        button.innerText = 'Скопировать';
        button.className = 'absolute top-2 right-2 px-2 py-1 text-xs bg-slate-800 border border-slate-700 rounded hover:border-brand hover:text-brand transition opacity-0 group-hover:opacity-100';
        button.addEventListener('click', () => {
            navigator.clipboard.writeText(codeBlock.innerText);
            button.innerText = 'Скопировано!';
            setTimeout(() => button.innerText = 'Скопировать', 1500);
        });
        pre.appendChild(button);
    });
</script>
</body>
</html>
