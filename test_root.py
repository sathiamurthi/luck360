import io
content = io.open('luck360_api_server.py', 'r', encoding='utf-8').read()
import re
m = re.search(r'@app\.get\("/".*?def', content, flags=re.DOTALL)
if m:
    print(content[m.start():m.start()+400].encode('ascii', 'ignore').decode('ascii'))
