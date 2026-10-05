import io
content = io.open('inject_js_final.py', 'r', encoding='utf-8').read()
print(content[:1500].encode('ascii', 'ignore').decode('ascii'))
