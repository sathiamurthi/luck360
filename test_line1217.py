import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
start = max(0, 1217 - 10)
end = min(len(content), 1217 + 10)
for i in range(start, end):
    print(f"{i+1}: {content[i].encode('ascii', 'ignore').decode('ascii')}")
