import io
content = io.open('index.html', 'r', encoding='utf-8').read()
idx = content.find("box-active-baseline")
if idx != -1:
    print("box-active-baseline found in index.html")
else:
    print("NOT FOUND!")
