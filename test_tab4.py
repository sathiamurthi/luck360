import io
content = io.open('index.html', 'r', encoding='utf-8').read()
idx = content.find("tab-kerala-content")
if idx != -1:
    print(content[idx:idx+1500].encode('ascii', 'ignore').decode('ascii'))
