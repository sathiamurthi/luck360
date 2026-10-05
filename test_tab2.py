import io
content = io.open('index.html', 'r', encoding='utf-8').read()
import re
m = re.search(r'id="tab-.*?kerala', content)
if m:
    print(content[m.start():m.start()+800].encode('ascii', 'ignore').decode('ascii'))
