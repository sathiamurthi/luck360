import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
start = 2920 - 1
for i in range(start, start + 30):
    print(f"{i+1}: {content[i].encode('ascii', 'ignore').decode('ascii')}")
