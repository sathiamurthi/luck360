import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("t.abc")
start = max(0, idx - 100)
end = min(len(content), idx + 200)
print(content[start:end].encode('ascii', 'ignore').decode('ascii'))
