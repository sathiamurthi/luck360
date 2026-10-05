import io
content = io.open('index.html', 'r', encoding='utf-8').read().splitlines()
for i, line in enumerate(content):
    if "910" in line:
        print(f"{i+1}: {line.strip()}")
