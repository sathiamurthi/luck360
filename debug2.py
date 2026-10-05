import sys
content = open('index.html', 'r', encoding='utf-8').read()
import re
scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
text = '\n'.join(scripts)
text = re.sub(r'//.*', '', text)
text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
text = re.sub(r'"(\\"|[^"])*"', '""', text)
text = re.sub(r"'(\\'|[^'])*'", "''", text)

print(text[5300:5500])
