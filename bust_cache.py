import io
import time

content = io.open('index.html', 'r', encoding='utf-8').read()
v = int(time.time())
content = content.replace('src="script1.js"', f'src="script1.js?v={v}"')
with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.html to bust cache!")
