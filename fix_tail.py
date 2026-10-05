import io
with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('prev.tail.slice(-3)', 'String(prev.result).slice(-3)')
content = content.replace('curr.tail.slice(-3)', 'String(curr.result).slice(-3)')

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
