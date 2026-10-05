import io
import re
content = io.open('script1.js', 'r', encoding='utf-8').read().splitlines()

for i, line in enumerate(content):
    if "addEventListener" in line and "$(" in line and "if (" not in line and "if(" not in line:
        print(f"{i+1}: {line.strip()}")
