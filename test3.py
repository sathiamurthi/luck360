import io
import re
content = io.open('index.html', 'r', encoding='utf-8').read()
m = re.search(r'function updateDashboard', content)
if m:
    print(content[m.start():m.start()+2000].encode('ascii', 'ignore').decode('ascii'))
