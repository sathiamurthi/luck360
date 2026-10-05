import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("const is8PMComplete")
div_start = content.rfind('function', 0, idx)
print(content[div_start:idx+150])
