import io
content = io.open('index.html', 'r', encoding='utf-8').read()
idx = content.find("tab-main-content")
print(content[idx:idx+1500].encode('ascii', 'ignore').decode('ascii'))
