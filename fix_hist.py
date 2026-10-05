import io
with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "if (hist && hist.length > 0) {",
    "if (typeof hist !== 'undefined' && hist && hist.length > 0) {"
)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
