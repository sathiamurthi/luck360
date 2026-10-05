import io

with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "NEXT DIRECT TARGETS</span>",
    "NEXT DIRECT TARGETS <span class=\"text-emerald-700\">(${nextDrawSlotName.toUpperCase()})</span></span>"
)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
