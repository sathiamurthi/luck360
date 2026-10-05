import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
start = max(0, 2908 - 5)
end = min(len(content), 2908 + 5)
for i in range(start, end):
    print(f"{i+1}: {content[i].encode('ascii', 'ignore').decode('ascii')}")
