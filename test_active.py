import io
import re
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("ACTIVE NEXT PLAY")
if idx != -1:
    print(content[max(0, idx-500):idx+1000].encode('ascii', 'ignore').decode('ascii'))
