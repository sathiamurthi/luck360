import io
content = io.open('index.html.bak', 'r', encoding='utf-8').read()
idx = content.find("ACTIVE BASELINE")
print(content[idx:idx+1500].encode('ascii', 'ignore').decode('ascii'))
