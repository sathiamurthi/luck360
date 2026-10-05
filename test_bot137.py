import io
content = io.open('index.html', 'r', encoding='utf-8').read().splitlines()
for line in content:
    if "mp-gaps" in line:
        print(line.strip())
