import io
import re
content = io.open('index.html', 'r', encoding='utf-8').read()
# Let's print all function names
matches = re.findall(r'function\s+(\w+)\s*\(', content)
print(list(set(matches)))
