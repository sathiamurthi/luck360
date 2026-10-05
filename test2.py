import io
import re
content = io.open('index.html', 'r', encoding='utf-8').read()
m = re.search(r'ACTIVE BASELINE|NEXT DIRECT TARGET', content, flags=re.IGNORECASE)
if m:
    print(content[max(0, m.start()-100) : m.start()+2000].encode('ascii', 'ignore').decode('ascii'))
else:
    print("Not found")
