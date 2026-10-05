import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
import re
m = re.search(r'h15_val.*?', content)
if m:
    print(content[m.start()-200:m.start()+200].encode('ascii', 'ignore').decode('ascii'))
