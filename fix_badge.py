import io
with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "document.getElementById('live-status-badge').innerHTML =",
    "if (document.getElementById('live-status-badge')) document.getElementById('live-status-badge').innerHTML ="
)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
