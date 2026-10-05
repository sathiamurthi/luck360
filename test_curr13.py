import io
import re

content = io.open('script1.js', 'r', encoding='utf-8').read()
missing = io.open('scratch/missing.js', 'r', encoding='utf-8').read()

# Find all function definitions in missing.js
funcs = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', missing)
for f in set(funcs):
    if f not in content:
        print(f"Missing function: {f}")
