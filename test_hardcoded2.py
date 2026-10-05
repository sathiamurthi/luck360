import io
content = io.open('index.html', 'r', encoding='utf-8').read()
import re
matches = re.findall(r'<tr>\s*<td.*?2026', content)
print(f"Found {len(matches)} hardcoded rows with 2026")
