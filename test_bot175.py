import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "const cardsContainer" in line or "let cardsContainer" in line or "var cardsContainer" in line:
        print(f"{i+1}: {line.strip()}")
