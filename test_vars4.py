import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
idx = content.find("is6PMComplete")
if idx != -1:
    print(content[max(0, idx-500):idx+500])
