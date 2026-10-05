import io
content = io.open('index.html', 'r', encoding='utf-8').read()
import re
matches = [m.start() for m in re.finditer("kerala chart", content.lower())]
for idx in matches:
    print("--- MATCH ---")
    print(content[max(0,idx-100):idx+500].encode('ascii', 'ignore').decode('ascii'))
