import io
content = io.open('index.html', 'r', encoding='utf-8').read()
idx = content.find("tab-kerala-content")
if idx != -1:
    print(content[idx+1500:idx+3000].encode('ascii', 'ignore').decode('ascii'))
