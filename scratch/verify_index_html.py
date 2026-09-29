import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Total size: {len(content)} characters")

# Check if script tags are balanced
script_open = len(re.findall(r'<script\b', content, re.IGNORECASE))
script_close = len(re.findall(r'</script>', content, re.IGNORECASE))
print(f"Script tags: <script={script_open}, </script>={script_close}")

# Check key keywords presence
for kw in ['h15_val', 'Star H15', 'Shift-Difference', 'winning_ab_patterns', 'table-historical-log', 'table-top-ab-pattern6']:
    count = content.count(kw)
    print(f"Keyword '{kw}': found {count} times")
