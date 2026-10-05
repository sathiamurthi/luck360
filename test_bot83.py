import io
content = io.open('index.html', 'r', encoding='utf-8').read().splitlines()
for line in content:
    if "script1.js" in line:
        print(line.strip())
