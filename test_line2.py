import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
idx = 3096 - 1
start = max(0, idx - 5)
end = min(len(content), idx + 5)
for i in range(start, end):
    print(f"{i+1}: {content[i]}")
