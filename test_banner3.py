import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("Dual Confluence")
if idx != -1:
    print(content[max(0, idx-100):idx+800].encode('ascii', 'ignore').decode('ascii'))
