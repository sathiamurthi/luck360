import io
content = io.open('index.html.bak', 'r', encoding='utf-8').read()
idx = content.find("box-active-baseline")
if idx != -1:
    print(content[max(0,idx-200):idx+200].encode('ascii', 'ignore').decode('ascii'))
