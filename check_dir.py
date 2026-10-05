import io
content = io.open('luck360_api_server.py', 'r', encoding='utf-8').read()
import re
print(re.findall(r'^[A-Z_]+ = .*os\.path.*', content, flags=re.MULTILINE))
