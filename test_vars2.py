import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("is3pmReflected")
print(content[max(0, idx-500):idx+500])
