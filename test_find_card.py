import io
content = io.open('index.html', 'r', encoding='utf-8').read()
idx = content.lower().find("currently running")
if idx != -1:
    print(content[max(0,idx-200):idx+300].encode('ascii', 'ignore').decode('ascii'))
