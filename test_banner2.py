import io
content = io.open('index.html', 'r', encoding='utf-8').read()
idx = content.find("Dual Confluence")
if idx != -1:
    print(content[max(0, idx-100):idx+1000].encode('ascii', 'ignore').decode('ascii'))
