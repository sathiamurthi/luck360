import io
content = io.open('index - Copy.html', 'r', encoding='utf-8').read()
idx = content.find("Today (25-Sep) &")
print(repr(content[idx-20:idx+40]))
