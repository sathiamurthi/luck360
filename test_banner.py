import io
content = io.open('index.html', 'r', encoding='utf-8').read()
idx = content.find("mp-banner")
if idx != -1:
    print(content[idx:idx+1500].encode('ascii', 'ignore').decode('ascii'))
