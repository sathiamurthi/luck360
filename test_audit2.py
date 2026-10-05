import io
content = io.open('index.html', 'r', encoding='utf-8').read()
idx = content.lower().find("kerala chart")
if idx != -1:
    print(content[max(0,idx-200):idx+800].encode('ascii', 'ignore').decode('ascii'))
