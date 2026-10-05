import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("Cross-Day Generated Targets")
print(content[idx:idx+3500].encode('ascii', 'ignore').decode('ascii'))
