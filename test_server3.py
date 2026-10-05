import io
import re
content = io.open('luck360_api_server.py', 'r', encoding='utf-8').read()
matches = re.findall(r'@app\.get\(.*?def.*?:', content, flags=re.DOTALL)
for m in matches:
    print(m.split('\n')[0])
