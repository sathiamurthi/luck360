import io
import re
content = io.open('index.html', 'r', encoding='utf-8').read()
if 'NEXT DIRECT TARGETS' in content:
    print("Found NEXT DIRECT TARGETS")
elif 'ACTIVE BASELINE' in content:
    print("Found ACTIVE BASELINE")
else:
    print("Neither found")
