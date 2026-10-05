import io
with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'let prevTail = String(prev.result).slice(-3);',
    'let prevTail = String(prev.result || "000").padStart(3, "0").slice(-3);'
).replace(
    'let currTail = String(curr.result).slice(-3);',
    'let currTail = String(curr.result || "000").padStart(3, "0").slice(-3);'
)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
