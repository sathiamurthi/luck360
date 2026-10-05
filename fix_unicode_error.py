import io

content = io.open('script1.js', 'r', encoding='utf-8').read()
content = content.replace(r'\U0001f3af', r'\u{1f3af}')
with io.open('script1.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed Invalid Unicode Escape!")
