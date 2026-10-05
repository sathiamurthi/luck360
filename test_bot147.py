import io
content = io.open('index.html', 'r', encoding='utf-8').read().splitlines()
for i in range(830, 880):
    print(f"{i+1}: {content[i].encode('ascii', 'ignore').decode('ascii')}")
