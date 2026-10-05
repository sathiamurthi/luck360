import io
content = io.open('luck360_api_server.py', 'r', encoding='utf-8').read()
import re
m = re.search(r'index\.html', content)
if m:
    print(content[max(0, m.start()-200):m.start()+200].encode('ascii', 'ignore').decode('ascii'))
