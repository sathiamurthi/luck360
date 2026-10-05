import io
with io.open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make activeResult fallback to something valid if null
content = content.replace(
    "const activeResult = calculateSingleDrawPatterns(activeBase);",
    "const activeResult = calculateSingleDrawPatterns(activeBase) || calculateSingleDrawPatterns('000');"
)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
