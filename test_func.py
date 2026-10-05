import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("Dual Confluence")
if idx != -1:
    div_start = content.rfind('function', 0, idx)
    print(content[div_start:idx+2500].encode('ascii', 'ignore').decode('ascii'))
