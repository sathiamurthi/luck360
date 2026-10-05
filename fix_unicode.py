import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
content = content.replace(r'\ud83c\udfaf', '\U0001f3af')
content = content.replace(r'\u00d7', '\u00d7')
with io.open('script1.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Replaced unicode escapes with direct characters")
