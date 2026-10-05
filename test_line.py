import io
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()
idx = 3125 - 1
start = max(0, idx - 10)
end = min(len(content), idx + 10)
for i in range(start, end):
    print(f"{i+1}: {content[i]}")
